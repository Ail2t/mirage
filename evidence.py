from dataclasses import dataclass, field

@dataclass
class Evidence:
    """Faits bruts observés par la sonde, ne contient aucun jugement :
    l'interprétation (le verdict) est faite séparément par rendre_verdict()"""    
    cible_vivante: bool = False # la cible répond-elle ?
    marqueur_present: bool = False # le marqueur de succès de l'exploit est-il dans la réponse ?
    details: dict = field(default_factory=dict) # infos brutes (status HTTP, taille réponse...)
    erreur: str | None = None
