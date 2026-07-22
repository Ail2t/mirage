from agent import extraire_fiche_ia, generer_sonde_ia, charger_sonde

# extraction de la fiche depuis le write-up XSS
writeup = open("../writeup_xss.txt").read()
fiche = extraire_fiche_ia(
    writeup,
    base_url="http://localhost:4280",
    actif="/vulnerabilities/xss_r/",
    param="name",
    security="low",
)

print("Fiche extraite :")
print(f"Description : {fiche.description}")
print(f"Payload     : {fiche.payload}")
print(f"Marqueur    : {fiche.marqueur_succes}")
print(f"Actif/param : {fiche.actif} / {fiche.param_injecte}")
print("-" * 60)

# génération de la sonde depuis la fiche

code = generer_sonde_ia(fiche)
print("Sonde générée :")
print(code)
