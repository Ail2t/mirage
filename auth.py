import requests

from bs4 import BeautifulSoup

USER="admin"
PASS="password"

def _extraire_token(html: str) -> str | None:
    # On récupère la valeur du champ caché user_token dans la page DVWA
    soup = BeautifulSoup(html, "html.parser")
    champ = soup.find("input", {"name": "user_token"})
    return champ["value"] if champ else None

def session_authentifiee(base_url: str, security: str) -> requests.Session:
    s = requests.Session()

    # On récupère le token et on pose le PHPSESSID

    r = s.get(f"{base_url}/login.php", timeout=10)
    token = _extraire_token(r.text)
    
    payload_login = {
            "username":USER,
            "password": PASS,
            "Login": "Login",
            "user_token": token or ""
            }

    r = s.post(f"{base_url}/login.php", data=payload_login, timeout=10, allow_redirects=True)
    
    # On vérifie si la connexion a réussie avec la présence de Logout sur la page
    if "Logout" in r.text:
        print("Connexion reussie")
    else:
        raise requests.RequestException("login échoué")
    
    # On pose le niveau de sécurité de DVWA pour les tests suivants
    r = s.get(f"{base_url}/security.php", timeout=10)
    token = _extraire_token(r.text)
    
    payload_sec = {
            "security": security,
            "seclev_submit": "Submit",
            "user_token": token or ""
            }

    s.post(f"{base_url}/security.php", data=payload_sec, timeout=10)
    print(f"Niveau de sécurité configuré sur : {security}")

    return s
