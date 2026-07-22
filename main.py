import os
import sys
import argparse

from agent import extraire_fiche_ia, generer_sonde_ia, charger_sonde

def main():
    parser = argparse.ArgumentParser(description="Vérification à partir d'un writeup brut")
    parser.add_argument("writeup", help="Fichier txt du writeup")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--actif", required=True, help="Chemin du module à tester")
    parser.add_argument("--param", required=True, help="Nom du paramètre HTTP à injecter")
    parser.add_argument("--security", default="low", help="Niveau voulu pour DVWA")
    parser.add_argument("--show-fiche", action="store_true", help="Affiche la fiche générée par IA")
    parser.add_argument("--runs", type=int, default=2)
    args = parser.parse_args()

    # On vérifie si la clé API est présente
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Clé API absente, le script nécessite l'API")
        sys.exit(1)
    
    # Lecture du writeup
    with open(args.writeup, encoding="utf-8") as f:
        writeup = f.read()

    # 1ère étape : extraction de la fiche depuis le writeup 
    print("L'agent IA extrait la fiche du writeup")
    try:
        fiche = extraire_fiche_ia(writeup, args.base_url.rstrip("/"), args.actif, args.param, args.security)
    except Exception as e:
        print(f"Echec de l'extraction : {e}")
        sys.exit(1)

    print("Fiche extraite : ", fiche.description)





if __name__ == "__main__":
    main()
