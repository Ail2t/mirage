import requests

from bs4 import BeautifulSoup

USER="admin"
PASS="password"

def _extraire_token(html: str) -> str | None:
    # On récupère la valeur du champ caché user_token dans la page DVWA
    soup = BeautifulSoup(html, "html.parser")
    champ = soup.find("input", {"name": "user_token"})
    return champ["value"] if champ else None

def session_authentifiee(base_url: str) -> requests.Session:
    s = requests.Session()

    # On récupère le token et on pose le PHPSESSID

    r = s.get(f"{base_url}/login.php", timeout=10)
    token = _extraire_token(r.text)
    
    payload = {
            "username":USER,
            "password": PASS,
            "Login": "Login",
            "user_token": token
            }

    r = s.post(f"{base_url}/login.php", data=payload, timeout=10, allow_redirects=True)

    if "Logout" in r.text:
        print("Connexion reussie")
    else:
        raise requests.RequestException("login échoué")

    return s
