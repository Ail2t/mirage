import requests

from bs4 import BeautifulSoup

LOGIN_URL="http://localhost:4280/login.php"
USER="admin"
PASS="password"

s = requests.Session()
response = s.get(LOGIN_URL, timeout=10)
soup = BeautifulSoup(response.text, "html.parser")

token = soup.find("input", attrs={"name": "user_token"})["value"]

print(f"Token récupéré : {token}")

payload = {
        "username":USER,
        "password": PASS,
        "Login": "Login",
        "user_token": token
        }

r = s.post(LOGIN_URL, data=payload, timeout=10)

if "Logout" in r.text:
    print("Connexion reussie")
else:
    print("Connexion refusée")
