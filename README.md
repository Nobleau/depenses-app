# 💰 Gestionnaire de Dépenses SQLite

Application Python minimaliste pour gérer ses dépenses personnelles,
conçue pour **apprendre les bases de GitHub** (commit, push, branches…).

---

## 🚀 Lancer l'application

```bash
python app.py
```

## 🧪 Lancer les tests

```bash
python test_app.py
```

---

## 📁 Structure du projet

```
depenses-app/
├── app.py          # Application principale (CRUD + CLI)
├── test_app.py     # Tests unitaires
├── depenses.db     # Base SQLite (créée au premier lancement)
└── README.md       # Ce fichier
```

---

## 🗄️ Schéma de la base de données

```
categories          depenses
──────────          ────────────────────────────
id   INTEGER PK     id           INTEGER PK
nom  TEXT            description  TEXT
                    montant      REAL
                    date         TEXT
                    categorie_id INTEGER → categories.id
```

---

## 🌿 Apprendre GitHub avec ce projet

### 1. Initialiser un dépôt

```bash
git init
git add .
git commit -m "feat: init gestionnaire de dépenses"
```

### 2. Créer une branche

```bash
git checkout -b feature/export-csv
# ... modifier le code ...
git add app.py
git commit -m "feat: ajouter export CSV"
git checkout main
git merge feature/export-csv
```

### 3. Pousser sur GitHub

```bash
git remote add origin https://github.com/TON_PSEUDO/depenses-app.git
git push -u origin main
```

### 4. Conventions de commit (Conventional Commits)

| Préfixe    | Usage                        |
|------------|------------------------------|
| `feat:`    | Nouvelle fonctionnalité      |
| `fix:`     | Correction de bug            |
| `docs:`    | Documentation                |
| `test:`    | Ajout/modification de tests  |
| `refactor:`| Refactoring sans bug fix     |

---

## 💡 Idées d'améliorations (pour pratiquer Git)

- [ ] Export CSV des dépenses
- [ ] Filtre par date (mois, année)
- [ ] Graphique ASCII des dépenses
- [ ] Import depuis un fichier CSV
- [ ] Interface web avec Flask

---

## 📄 Licence

MIT — libre d'utilisation et de modification.
