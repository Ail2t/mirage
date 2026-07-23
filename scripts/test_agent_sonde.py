from agent import generer_sonde_ia, Fiche

# Une fiche de test (objet Pydantic, comme le renvoie l'étage 1)
fiche = Fiche(
    description="XSS réfléchie de test",
    payload="<script>alert(1)</script>",
    marqueur_succes="<script>alert(1)</script>",
    actif="/vulnerabilities/xss_r/",
    param_injecte="name",
    base_url="http://localhost:4280",
    dvwa_security="low",
)

code = generer_sonde_ia(fiche)

print("Sonde générée par IA")
print(code)
