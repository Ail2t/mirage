from agent import extraire_fiche_ia

CAS = [
    ("../writeup_xss.txt", "/vulnerabilities/xss_r/", "name", "low"),
    ("../writeup_sqli.txt", "/vulnerabilities/sqli/", "id", "low"),
    ("../writeup_fileinclusion.txt", "/vulnerabilities/fi/", "page", "low"),
]

for chemin, actif, param, security in CAS:
    writeup = open(chemin).read()
    fiche = extraire_fiche_ia(writeup, "http://localhost:4280", actif, param, security)
    print(f"Write-up      : {chemin}")
    print(f"Description   : {fiche.description}")
    print(f"Payload       : {fiche.payload}")
    print(f"Marqueur      : {fiche.marqueur_succes}")
    print(f"Actif / param : {fiche.actif} / {fiche.param_injecte}")
