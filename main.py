import os
import sys
import argparse
import requests

from auth import session_authentifiee
from verdict import rendre_verdict
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
    
    # Ajout de la fiche si option
    if args.show_fiche:
        print("Fiche extraite par l'IA :")
        print(fiche.model_dump_json(indent=2))

    # 2ème étape : génération de la sonde depuis la fiche
    print("L'agent IA génère la sonde")
    try:
        code = generer_sonde_ia(fiche)
    except Exception as e:
        print(f"Echec de la génération : {e}")
        sys.exit(1)

    # Affichage de la sonde générée avec validation humaine avant exécution
    print("\nSonde générée :")
    print(code)
    print("─────────────────────")
    reponse = input("Exécuter cette sonde ? [o/N] ")
    if reponse.strip().lower() != "o":
        print("Exécution annulée")
        sys.exit(0)

    probe = charger_sonde(code)
    print("Sonde chargée avec succès")


if __name__ == "__main__":
    main()
