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

