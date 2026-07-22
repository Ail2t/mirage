import anthropic

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

client = anthropic.Anthropic()

message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Décris une sqli"
            }]
        )

print(message.content[0].text)
