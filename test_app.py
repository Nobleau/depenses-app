"""
Tests unitaires pour le gestionnaire de dépenses.
Lancez avec : python test_app.py
"""

import unittest
import os
import app  # notre module principal


class TestDepenses(unittest.TestCase):

    def setUp(self):
        """Avant chaque test : utiliser une BDD de test."""
        app.DB_NAME = "test_depenses.db"
        app.creer_tables()

    def tearDown(self):
        """Après chaque test : supprimer la BDD de test."""
        if os.path.exists(app.DB_NAME):
            os.remove(app.DB_NAME)

    def test_ajouter_et_lister(self):
        dep_id = app.ajouter("Café", 150, 1)
        self.assertGreater(dep_id, 0)

        rows = app.lister()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["description"], "Café")
        self.assertAlmostEqual(rows[0]["montant"], 150)

    def test_modifier(self):
        dep_id = app.ajouter("Bus", 80, 2)
        ok = app.modifier(dep_id, description="Taxi", montant=200)
        self.assertTrue(ok)

        rows = app.lister()
        self.assertEqual(rows[0]["description"], "Taxi")
        self.assertAlmostEqual(rows[0]["montant"], 200)

    def test_supprimer(self):
        dep_id = app.ajouter("Ciné", 500, 5)
        ok = app.supprimer(dep_id)
        self.assertTrue(ok)
        self.assertEqual(len(app.lister()), 0)

    def test_total(self):
        app.ajouter("Pain", 50, 1)
        app.ajouter("Lait", 100, 1)
        self.assertAlmostEqual(app.total(), 150)

    def test_stats_par_categorie(self):
        app.ajouter("Pain", 50, 1)   # Alimentation
        app.ajouter("Taxi", 200, 2)  # Transport
        stats = app.stats_par_categorie()
        # Transport doit être en premier (plus grand total)
        self.assertEqual(stats[0]["total"], 200)

    def test_modifier_id_inexistant(self):
        ok = app.modifier(9999, description="Ghost")
        self.assertFalse(ok)

    def test_supprimer_id_inexistant(self):
        ok = app.supprimer(9999)
        self.assertFalse(ok)

    def test_filtre_categorie(self):
        app.ajouter("Pain", 50, 1)
        app.ajouter("Bus", 80, 2)
        rows = app.lister(categorie_id=1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["description"], "Pain")


if __name__ == "__main__":
    unittest.main(verbosity=2)
