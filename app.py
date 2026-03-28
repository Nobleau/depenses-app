"""
Gestionnaire de Dépenses - SQLite
Application simple pour apprendre SQLite avec Python
"""

import sqlite3
from datetime import datetime


DB_NAME = "depenses.db"


def connexion():
    """Créer ou ouvrir la base de données."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Accès par nom de colonne
    return conn


def creer_tables():
    """Créer les tables si elles n'existent pas."""
    conn = connexion()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            nom     TEXT NOT NULL UNIQUE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS depenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT    NOT NULL,
            montant     REAL    NOT NULL CHECK(montant > 0),
            date        TEXT    NOT NULL,
            categorie_id INTEGER REFERENCES categories(id)
        )
    """)
    # Catégories par défaut
    for cat in ("Alimentation", "Transport", "Logement", "Santé", "Loisirs", "Autre"):
        conn.execute("INSERT OR IGNORE INTO categories (nom) VALUES (?)", (cat,))
    conn.commit()
    conn.close()


# ── CRUD Dépenses ──────────────────────────────────────────────────────────────

def ajouter(description, montant, categorie_id, date=None):
    """Ajouter une dépense."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    conn = connexion()
    cur = conn.execute(
        "INSERT INTO depenses (description, montant, date, categorie_id) VALUES (?,?,?,?)",
        (description, montant, date, categorie_id)
    )
    conn.commit()
    conn.close()
    return cur.lastrowid


def lister(categorie_id=None):
    """Lister toutes les dépenses (avec filtre optionnel)."""
    conn = connexion()
    if categorie_id:
        rows = conn.execute("""
            SELECT d.id, d.description, d.montant, d.date, c.nom AS categorie
            FROM depenses d LEFT JOIN categories c ON d.categorie_id = c.id
            WHERE d.categorie_id = ?
            ORDER BY d.date DESC
        """, (categorie_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT d.id, d.description, d.montant, d.date, c.nom AS categorie
            FROM depenses d LEFT JOIN categories c ON d.categorie_id = c.id
            ORDER BY d.date DESC
        """).fetchall()
    conn.close()
    return rows


def modifier(dep_id, description=None, montant=None, categorie_id=None):
    """Modifier une dépense existante."""
    conn = connexion()
    row = conn.execute("SELECT * FROM depenses WHERE id=?", (dep_id,)).fetchone()
    if not row:
        conn.close()
        return False
    description   = description   or row["description"]
    montant       = montant       or row["montant"]
    categorie_id  = categorie_id  or row["categorie_id"]
    conn.execute(
        "UPDATE depenses SET description=?, montant=?, categorie_id=? WHERE id=?",
        (description, montant, categorie_id, dep_id)
    )
    conn.commit()
    conn.close()
    return True


def supprimer(dep_id):
    """Supprimer une dépense."""
    conn = connexion()
    cur = conn.execute("DELETE FROM depenses WHERE id=?", (dep_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


# ── Statistiques ───────────────────────────────────────────────────────────────

def total():
    """Total général."""
    conn = connexion()
    row = conn.execute("SELECT COALESCE(SUM(montant),0) AS total FROM depenses").fetchone()
    conn.close()
    return row["total"]


def stats_par_categorie():
    """Dépenses groupées par catégorie."""
    conn = connexion()
    rows = conn.execute("""
        SELECT c.nom AS categorie, COUNT(*) AS nb, SUM(d.montant) AS total
        FROM depenses d
        JOIN categories c ON d.categorie_id = c.id
        GROUP BY c.id
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return rows


def categories():
    """Retourner toutes les catégories."""
    conn = connexion()
    rows = conn.execute("SELECT * FROM categories ORDER BY nom").fetchall()
    conn.close()
    return rows


# ── Interface CLI ──────────────────────────────────────────────────────────────

def afficher_menu():
    print("\n" + "═"*40)
    print("  💰 Gestionnaire de Dépenses SQLite")
    print("═"*40)
    print("  1. Voir toutes les dépenses")
    print("  2. Ajouter une dépense")
    print("  3. Modifier une dépense")
    print("  4. Supprimer une dépense")
    print("  5. Statistiques par catégorie")
    print("  6. Quitter")
    print("═"*40)


def afficher_depenses(rows):
    if not rows:
        print("  (aucune dépense)")
        return
    print(f"\n{'ID':>4}  {'Date':<12}  {'Catégorie':<14}  {'Montant':>10}  Description")
    print("─"*65)
    for r in rows:
        print(f"  {r['id']:>2}  {r['date']:<12}  {r['categorie'] or '?':<14}  {r['montant']:>8.2f} DA  {r['description']}")
    print("─"*65)
    print(f"  Total : {sum(r['montant'] for r in rows):.2f} DA\n")


def choisir_categorie():
    cats = categories()
    print("\n  Catégories :")
    for c in cats:
        print(f"    {c['id']}. {c['nom']}")
    while True:
        try:
            cid = int(input("  Numéro de catégorie : "))
            if any(c["id"] == cid for c in cats):
                return cid
            print("  ❌ Numéro invalide.")
        except ValueError:
            print("  ❌ Entrez un nombre.")


def run():
    creer_tables()
    while True:
        afficher_menu()
        choix = input("  Votre choix : ").strip()

        if choix == "1":
            afficher_depenses(lister())

        elif choix == "2":
            desc = input("  Description : ").strip()
            try:
                mont = float(input("  Montant (DA) : "))
            except ValueError:
                print("  ❌ Montant invalide.")
                continue
            cid = choisir_categorie()
            dep_id = ajouter(desc, mont, cid)
            print(f"  ✅ Dépense #{dep_id} ajoutée.")

        elif choix == "3":
            afficher_depenses(lister())
            try:
                dep_id = int(input("  ID à modifier : "))
            except ValueError:
                continue
            desc  = input("  Nouvelle description (Entrée = garder) : ").strip() or None
            mont_s = input("  Nouveau montant (Entrée = garder) : ").strip()
            mont  = float(mont_s) if mont_s else None
            print("  Nouvelle catégorie :")
            cid = choisir_categorie()
            if modifier(dep_id, desc, mont, cid):
                print("  ✅ Dépense mise à jour.")
            else:
                print("  ❌ ID introuvable.")

        elif choix == "4":
            afficher_depenses(lister())
            try:
                dep_id = int(input("  ID à supprimer : "))
            except ValueError:
                continue
            conf = input(f"  Supprimer #{dep_id} ? (o/n) : ").lower()
            if conf == "o":
                if supprimer(dep_id):
                    print("  ✅ Dépense supprimée.")
                else:
                    print("  ❌ ID introuvable.")

        elif choix == "5":
            print(f"\n  Total général : {total():.2f} DA\n")
            print(f"  {'Catégorie':<16}  {'Nb':>4}  {'Total':>10}")
            print("  " + "─"*35)
            for r in stats_par_categorie():
                print(f"  {r['categorie']:<16}  {r['nb']:>4}  {r['total']:>8.2f} DA")

        elif choix == "6":
            print("\n  Au revoir ! 👋\n")
            break
        else:
            print("  ❌ Choix invalide.")


if __name__ == "__main__":
    run()
