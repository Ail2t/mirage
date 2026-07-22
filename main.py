



def main():
    parser = argparse.ArgumentParser(description="Vérification à partir d'un writeup brut")
    parser.add_argument("writeup", help="Fichier txt du writeup")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--actif", required=True, help="Chemin du module à tester")
    parser.add_argument("--param", required=True, help="Nom du paramètre HTTP à injecter")
    parser.add_argument("--security", default="low", help="Niveau voulu pour DVWA")
    parser.add_argument("--show-fiche", action="store_true", help="Affiche la fiche générée par IA")
    args = parse.parser_args()
