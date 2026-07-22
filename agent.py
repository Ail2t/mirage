import re

from pydantic import BaseModel

class Fiche(BaseModel):
    """Champs fournis par l'agent"""
    # Description de la vuln
    description: str
    # L'injection qui correspond à la vuln
    payload: str
    # La chaine qui prouve le succes de l'exploit
    marqueur_succes: str
    # Les paramètres annexes comme submit pour la SQLi
    params_base: dict = {}
    # Puis les champs fournis manuellement
    base_url: str = ""
    dvwa_security: str = ""
    # Le chemin du module à tester
    actif: str = ""
    # Le paramètre à injecter dans le module
    param_injecte: str = ""

PROMPT_EXTRACTION = """Tu extrais une fiche de vulnérabilité structurée à partir d'un write-up brut (prose).

On te donne :
  - le TEXTE d'un write-up décrivant une vulnérabilité web et son exploitation ;
  - un CONTEXTE CIBLE fournissant les coordonnées techniques que le write-up
    ne contient pas (actif = chemin du module, param_injecte = nom du paramètre HTTP).

Tu produis UNIQUEMENT un objet JSON valide, sans texte autour, avec ces clés :
  - "description"    : phrase courte décrivant la vulnérabilité.
  - "actif"          : reprends EXACTEMENT la valeur du contexte cible.
  - "param_injecte"  : reprends EXACTEMENT la valeur du contexte cible.
  - "payload"        : le payload d'exploitation, extrait littéralement du write-up.
  - "marqueur_succes": la chaîne dont la PRÉSENCE dans la réponse HTTP prouve
    que l'exploit a fonctionné. Règle selon le type de vuln :
      * exfiltration de données (SQLi UNION, etc.) -> la donnée exfiltrée.
      * XSS réfléchie -> le payload lui-même, car en l'absence de filtrage il
        est réfléchi TEL QUEL (non-encodé) dans la réponse ; sa présence
        littérale prouve l'absence d'encodage, donc la vulnérabilité.

Réponds avec le JSON SEULEMENT : pas de ```, pas de commentaire, pas de prose.
"""

def extraire_fiche_ia(writeup: str, base_url: str, actif: str, param: str, security: str) -> Fiche:
    import anthropic
    client = anthropic.Anthropic()
    contexte = (f"CONTEXTE CIBLE : \n"
                f"  actif = {actif}\n"
                f"  param_injecte = {param}\n\n"
                f"WRITE-UP : \n{writeup}")
    msg = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system=PROMPT_EXTRACTION,
            messages=[{"role": "user", "content": contexte}],
            )
    # Nettoyage
    raw = "".join(b.text for b in msg.content if b.type == "text").strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    
    # Validation Pydantic
    try:
        fiche = Fiche.model_validate_json(raw)
    except ValidationError as e:
        raise RuntimeError(f"Fiche invalide extraite par l'IA : {e}")
    
    fiche.base_url = base_url
    fiche.dvwa_security = security
    fiche.actif = actif
    fiche.param_injecte = param
    return fiche


PROMPT_SONDE = """Tu es un générateur de sondes de revérification de vulnérabilités web (boîte noire).

On te donne une fiche de vulnérabilité (JSON). Tu produis UNIQUEMENT le corps
d'une fonction Python nommée `probe`, sans rien d'autre.

Signature imposée :
    def probe(session, base_url, fiche):

Contrat STRICT :
  - `session` est un requests.Session DÉJÀ authentifié. Ne fais PAS de login.
  - Tu collectes des FAITS et remplis un Evidence. Tu ne JUGES RIEN.
    Evidence(cible_vivante: bool, marqueur_present: bool, details: dict, erreur: str|None)
  - Étape 1 — liveness : UNE requête GET sur base_url + fiche["actif"] avec
    fiche.get("params_base", {}), SANS payload. Si status_code < 500 -> vivante.
    Sinon renvoie Evidence(cible_vivante=False, erreur=...) et arrête-toi.
  - Étape 2 — exploit : reprends params_base, mets fiche["payload"] dans le
    paramètre fiche["param_injecte"], envoie la requête. marqueur_present=True
    UNIQUEMENT si fiche["marqueur_succes"] apparaît dans r.text.
  - Enveloppe chaque requête dans try/except requests.RequestException. Pour
    l'exploit en cas d'exception : Evidence(cible_vivante=True,
    marqueur_present=False, erreur=str(e)). Ne conclus JAMAIS "corrigé".
  - AUCUN import. `requests` et `Evidence` sont déjà disponibles.
  - Réponds avec le CODE SEULEMENT : pas de texte, pas de ```.
"""

def generer_sonde_ia(fiche: Fiche) -> str:
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            system=PROMPT_SONDE,
            messages=[{"role": "user", "content": "Fiche :\n\n" + fiche.model_dump_json(indent=2)}],
            )
    code = "".join(b.text for b in msg.content if b.type == "text").strip()
    code = re.sub(r"^```(?:python)?\s*", "", code)
    code = re.sub(r"\s*```$", "", code)
    return code
