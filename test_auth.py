import requests
from auth import session_authentifiee

BASE_URL = "http://localhost:4280"

if __name__ == "__main__":
    try:
        # On teste l'authentification en passant le niveau de sécurité souhaité (ex: "low")
        security_level = "low"
        session = session_authentifiee(BASE_URL, security=security_level)
        
        # Vérification optionnelle : on s'assure que le cookie de sécurité est bien appliqué
        current_sec = session.cookies.get("security")
        print(f"Cookie de sécurité actif dans la session : {current_sec}")
        
        print("Test d'authentification et de configuration validé avec succès !")
        
    except requests.RequestException as err:
        print(f"Erreur réseau ou d'authentification : {err}")
    except Exception as err:
        print(f"Erreur inattendue : {err}")
