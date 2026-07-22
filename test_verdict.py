import unittest
from evidence import Evidence
from verdict import rendre_verdict


class TestVerdict(unittest.TestCase):

    def test_cible_non_vivante(self):
        """Teste le cas où la cible ne répond pas."""
        e = Evidence(
            cible_vivante=False,
            erreur="Connection refused"
        )
        verdict, raison = rendre_verdict(e)
        
        self.assertEqual(verdict, "INDETERMINE")
        self.assertIn("cible non vivante ou injoignable", raison)

    def test_erreur_technique(self):
        """Teste le cas où la cible est vivante mais un problème technique survient."""
        e = Evidence(
            cible_vivante=True,
            erreur="Timeout lors du POST"
        )
        verdict, raison = rendre_verdict(e)
        
        self.assertEqual(verdict, "INDETERMINE")
        self.assertIn("l'exploit a échoué techniquement", raison)

    def test_vulnerable(self):
        """Teste le cas où le marqueur d'exploitation est détecté."""
        e = Evidence(
            cible_vivante=True,
            marqueur_present=True
        )
        verdict, raison = rendre_verdict(e)
        
        self.assertEqual(verdict, "VULNERABLE")
        self.assertIn("le marqueur d'exploitation est apparu", raison)

    def test_corrige(self):
        """Teste le cas où la cible répond sans marqueur ni erreur."""
        e = Evidence(
            cible_vivante=True,
            marqueur_present=False
        )
        verdict, raison = rendre_verdict(e)
        
        self.assertEqual(verdict, "CORRIGE")
        self.assertIn("la cible répond normalement mais l'exploit n'est plus efficace", raison)


if __name__ == "__main__":
    unittest.main()
