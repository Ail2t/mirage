from evidence import Evidence 

def rendre_verdict(e: Evidence) -> tuple[str, str]:
    # Si la cible est morte ou injoignable
    if not e.cible_vivante:
        return "INDETERMINE", f"cible non vivante ou injoignable (erreur : {e.erreur})"

    # Si la cible est vivante mais l'exploit à un problème technique
    if e.erreur:
        return "INDETERMINE", f"cible vivante mais l'exploit a échoué techniquement (erreur : {e.erreur})"

    # Si le marqueur est présent, l'exploit est efficace
    if e.marqueur_present: 
        return "VULNERABLE", "le marqueur d'exploitation est apparu dans la réponse"

    # Si la cible est vivante et on ne voit ni erreur ni marqueur
    return "CORRIGE", "la cible répond normalement mais l'exploit n'est plus efficace"
