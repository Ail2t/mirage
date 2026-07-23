import unittest
from agent import charger_sonde


class TestChargerSonde(unittest.TestCase):

    def test_code_valide_retourne_callable(self):
        """Un code définissant probe() doit renvoyer une fonction appelable."""
        code = (
            "def probe(session, base_url, fiche):\n"
            "    return Evidence(cible_vivante=True, marqueur_present=True)\n"
        )
        probe = charger_sonde(code)
        self.assertTrue(callable(probe))

    def test_probe_utilise_evidence_et_requests_injectes(self):
        """probe() doit pouvoir utiliser Evidence sans import (injecté par charger_sonde)."""
        code = (
            "def probe(session, base_url, fiche):\n"
            "    ev = Evidence(cible_vivante=True, marqueur_present=False)\n"
            "    ev.details['ok'] = True\n"
            "    return ev\n"
        )
        probe = charger_sonde(code)
        resultat = probe(None, "http://x", {})
        self.assertTrue(resultat.cible_vivante)
        self.assertFalse(resultat.marqueur_present)
        self.assertEqual(resultat.details, {"ok": True})

    def test_code_sans_probe_leve_runtimeerror(self):
        """Un code qui ne définit aucune fonction probe doit lever RuntimeError."""
        code = "x = 42\n"
        with self.assertRaises(RuntimeError):
            charger_sonde(code)

    def test_code_avec_mauvais_nom_leve_runtimeerror(self):
        """Une fonction au mauvais nom ne compte pas comme probe."""
        code = (
            "def sonde(session, base_url, fiche):\n"
            "    return None\n"
        )
        with self.assertRaises(RuntimeError):
            charger_sonde(code)

    def test_code_invalide_leve_erreur(self):
        """Un code Python syntaxiquement invalide doit lever une erreur à l'exec."""
        code = "def probe(:\n"  # syntaxe cassée
        with self.assertRaises(SyntaxError):
            charger_sonde(code)


if __name__ == "__main__":
    unittest.main()
