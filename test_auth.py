from auth import session_authentifiee

BASE_URL = "http://localhost:4280"

if __name__ == "__main__":
    try:
        session = session_authentifiee(BASE_URL)
        print("[+] Test d'authentification validé avec succès !")
    except Exception as err:
        print(f"[-] Erreur lors du test : {err}")
