# MongoDB Data Migration Pipeline
Ce projet implémente une pipeline de migration de données à partir d'un fichier CSV (`healthcare_dataset.csv`) vers une base de données MongoDB, avec des tests unitaires et d'intégration pour valider le processus. Il utilise Docker pour gérer les services (MongoDB, migration, tests) et Poetry pour la gestion des dépendances Python dans les conteneurs. Le script principal traite le fichier CSV, applique des transformations (normalisation, calcul de durées), et migre les données (par exemple, 55 500 documents) vers une collection MongoDB. Les tests utilisent `mongomock` pour simuler l'insertion de 3 documents.

## Table des matières
- [Prérequis](#prérequis)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Exécution de la migration](#exécution-de-la-migration)
- [Processus de migration](#processus-de-migration)
- [Tests](#tests)
- [Dépannage](#dépannage)

## Prérequis
Pour exécuter ce projet localement, assurez-vous d'avoir installé :
- **Docker** : Pour exécuter les conteneurs MongoDB, migration, et tests.
- **Docker Compose** : Pour orchestrer les services.
- **Git** : Pour cloner le dépôt.
- **Poetry** (optionnel) : Requis uniquement pour exécuter le projet hors Docker.

## Structure du projet
```
p5-de/
├── .env                    # Variables d'environnement (ex. : identifiants MongoDB)
├── Dockerfile              # Configuration de l'image Docker pour l'application
├── docker-compose.yml      # Orchestration des services (mongo, app, test)
├── init-mongo/             # Scripts d'initialisation MongoDB
│   └── init-mongo.sh       # Crée l'utilisateur app_user pour la base healthcare
├── poetry.lock             # Verrouillage des dépendances Poetry
├── pyproject.toml          # Configuration Poetry et dépendances
├── data/                   # Données d'entrée
│   └── healthcare_dataset.csv  # Fichier CSV contenant les données à migrer
├── src/                    # Code source principal
│   ├── main.py             # Point d'entrée pour la migration
│   ├── utils/              # Utilitaires
│   │   └── envconf.py      # Charge les variables d'environnement
│   └── pipelines/          # Scripts de pipeline
│       ├── migrate_data.py # Logique de migration vers MongoDB
│       └── process_data.py # Traitement du fichier CSV
├── tests/                  # Tests unitaires et d'intégration
│   ├── integration/        # Tests d'intégration avec mongomock
│   │   └── test_migrate_data.py
│   └── unit/               # Tests unitaires
│       └── test_process_data.py
└── README.md               # Ce fichier
```

## Installation
1. **Cloner le dépôt** :
   ```bash
   git clone <url-du-dépôt>
   cd p5-de
   ```

2. **Configurer les variables d’environnement** :
   Créez un fichier `.env` à la racine du projet avec le contenu suivant :
   ```
   ROOT_USERNAME=admin
   ROOT_PASSWORD=admin123
   MONGO_APP_USER=app_user
   MONGO_APP_PASSWORD=app_pw
   MONGO_DB=healthcare
   MONGO_COL=patients
   ```
   Ces variables définissent les identifiants MongoDB, la base de données cible (`healthcare`), et la collection (`patients`).

3. **Vérifier la présence du fichier CSV** :
   Assurez-vous que `data/healthcare_dataset.csv` existe. Ce fichier contient les données à migrer (par exemple, informations sur les patients comme `name`, `age`, `admission_date`, `discharge_date`).

4. **Installer les dépendances (optionnel, pour exécution hors Docker)** :
   Si vous souhaitez exécuter le projet localement sans Docker (par exemple, pour déboguer ou lancer les tests), assurez-vous que Poetry est installé et exécutez :
   ```bash
   poetry install
   ```
   Cela installe les dépendances définies dans `pyproject.toml` dans un environnement virtuel.

## Exécution de la migration
Pour lancer la migration des données du fichier CSV vers MongoDB :

1. **Construire et exécuter les services avec Docker Compose** :
   ```bash
   docker compose up --build
   ```

   Cela démarre trois services :
   - **mongo** : Une instance MongoDB avec la base `healthcare` et l’utilisateur `app_user`.
   - **mongo-mig** : Exécute `src/main.py` pour traiter le fichier CSV et migrer les données.
   - **mongo-test** : Exécute les tests unitaires et d'intégration avec pytest.

2. **Sortie attendue** :
   - Dans les logs de `mongo-mig` :
     ```
     mongo-mig   | 55500 documents insérés
     mongo-mig exited with code 0
     ```
   - Dans les logs de `mongo-test` :
     ```
     mongo-test  | ============================= test session starts ==============================
     mongo-test  | platform linux -- Python 3.11.14, pytest-8.4.2, pluggy-1.6.0
     mongo-test  | ...
     mongo-test  | DataFrame après process_data:
     mongo-test  |           name  age date_of_birth admission_date discharge_date  patient_id  duration_days
     mongo-test  | 0     John Doe   30    1993-05-15     2023-10-01     2023-10-05           1              4
     mongo-test  | 1    Jane Smith   40    1983-07-20     2023-10-02     2023-10-07           2              5
     mongo-test  | 2   Alice Brown   25    1998-07-20     2023-10-03     2023-10-08           3              5
     mongo-test  | 3    Bob Wilson   35           NaT     2023-10-04     2023-10-09           4              5
     mongo-test  | Assertion passed: DataFrame length is 4
     mongo-test  | Assertion passed: duration_days for John Doe is 4
     mongo-test  | Assertion passed: duration_days for Jane Smith is 5
     mongo-test  | tests/unit/test_process_data.py::test_process_data PASSED [50%]
     mongo-test  | 3 documents insérés
     mongo-test  | Assertion passed: 3 documents insérés
     mongo-test  | tests/integration/test_migrate_data.py::test_migrate_data PASSED [100%]
     mongo-test  | ============================= 2 passed in 1.34s ===============================
     mongo-test exited with code 0
     ```

3. **Arrêter les services** :
   ```bash
   docker compose down -v
   ```

## Processus de migration
Le processus de migration est géré par les scripts `src/main.py`, `src/pipelines/process_data.py`, et `src/pipelines/migrate_data.py`. Voici ce qui se passe pendant la migration :

1. **Initialisation de MongoDB** :
   - Le service `mongo` démarre une instance MongoDB (version 6.0.26).
   - Le script `init-mongo/init-mongo.sh` crée un utilisateur `app_user` avec des droits de lecture/écriture sur la base `healthcare`.
   - Les variables d’environnement (`MONGO_APP_USER`, `MONGO_APP_PASSWORD`, `MONGO_DB`, `MONGO_COL`) sont chargées depuis `.env` via `src/utils/envconf.py`.

2. **Traitement des données (src/pipelines/process_data.py)** :
   - La fonction `process_data` est appelée dans `src/main.py` avec le chemin du fichier `data/healthcare_dataset.csv`.
   - Étapes effectuées par `process_data` :
     - **Chargement du CSV** : Lit le fichier CSV avec `pandas.read_csv`, en ignorant les lignes mal formées (`on_bad_lines='skip'`).
     - **Normalisation des colonnes** : Convertit les noms de colonnes en minuscules, remplace les espaces et points par des underscores (ex. : `Admission Date` devient `admission_date`).
     - **Détection des types** : Identifie automatiquement les colonnes de type chaîne, numérique, et date si non spécifiées.
     - **Transformation des chaînes** : Applique une transformation (par défaut `title`) sur les colonnes de chaînes, supprime les guillemets, réduit les espaces multiples, et supprime les espaces aux extrémités.
     - **Conversion des types** : Convertit les colonnes numériques en `int64`/`float64` et les colonnes de dates en `datetime`.
     - **Calcul de la durée** : Si spécifié (par exemple, `admission_date`, `discharge_date`, `duration_days`), calcule la durée en jours entre deux colonnes de dates.
     - **Suppression des NaN** : Supprime les lignes avec des valeurs manquantes dans les colonnes requises, si spécifiées.
   - Retourne un DataFrame pandas nettoyé et transformé.

3. **Migration des données (mongo-mig)** :
   - Le service `mongo-mig` exécute `src/main.py`, qui :
     - Charge les variables d’environnement via `get_vars()` dans `src/utils/envconf.py`.
     - Établit une connexion MongoDB avec `get_mongo_client`, utilisant les variables `mongo_host` (`mongo`), `mongo_port` (27017), `mongo_db` (`healthcare`), `mongo_user` (`app_user`), et `mongo_password` (`app_pw`).
     - Appelle `process_data` pour traiter `healthcare_dataset.csv`.
     - Passe le DataFrame résultant à `migrate_data` avec le client MongoDB, la base `healthcare`, et la collection `patients`.
   - Dans `migrate_data` :
     - Se connecte à la collection `patients` dans la base `healthcare`.
     - Insère les données du DataFrame (par exemple, 55 500 documents) dans MongoDB.
     - Affiche un message comme `55500 documents insérés` dans les logs.

4. **Tests (mongo-test)** :
   - Le service `mongo-test` exécute `pytest tests/ -v -s` pour lancer les tests unitaires et d'intégration.
   - **Test unitaire (`tests/unit/test_process_data.py`)** :
     - Crée un DataFrame fictif avec 4 enregistrements (patients).
     - Valide le traitement des données (normalisation, calcul de `duration_days`).
     - Vérifie que le DataFrame a 4 lignes et que les durées pour les patients 1 et 2 sont correctes (4 et 5 jours).
     - Affiche le DataFrame et des messages pour chaque assertion réussie (ex. : `Assertion passed: DataFrame length is 4`).
   - **Test d’intégration (`tests/integration/test_migrate_data.py`)** :
     - Utilise `mongomock` pour simuler une base MongoDB.
     - Appelle `migrate_data` avec `host="localhost"` pour insérer 3 documents fictifs.
     - Vérifie que 3 documents sont insérés et affiche un message comme `Assertion passed: 3 documents insérés`.

5. **Sortie des logs** :
   - Les logs incluent les résultats des tests, les `print()` des assertions réussies, le DataFrame traité, et le message de `mongo-mig` confirmant l’insertion des 55 500 documents.
   - La variable `PYTHONUNBUFFERED=1` garantit que les sorties sont immédiatement visibles dans les logs Docker.
   - L’option `-s` dans pytest permet l’affichage des `print()` dans `mongo-test`.

## Tests
Pour exécuter les tests manuellement dans un conteneur Docker :
```bash
docker compose run mongo-test
```

Pour exécuter les tests localement hors Docker (nécessite Poetry et Python 3.11) :
```bash
poetry run pytest tests/ -v -s
```

- Les tests unitaires vérifient le traitement des données dans un DataFrame pandas (normalisation, conversions, calcul de durées).
- Les tests d’intégration valident l’insertion de données dans MongoDB via `mongomock`.
- Les logs affichent les DataFrames, les documents insérés, et les messages des assertions réussies.

## Dépannage
- **Problème : Les `print()` ne s’affichent pas dans les logs** :
  - Vérifiez que `PYTHONUNBUFFERED=1` est défini dans `docker-compose.yml`.
  - Assurez-vous que l’option `-s` est incluse dans la commande pytest (`bash -c "export PYTHONPATH=/app && poetry run pytest tests/ -v -s"`).
- **Problème : Erreur de connexion MongoDB** :
  - Vérifiez que le service `mongo` est démarré avant `mongo-mig` et `mongo-test` (géré par `depends_on`).
  - Confirmez que les variables dans `.env` correspondent à celles dans `init-mongo.sh`.
- **Problème : Fichier `healthcare_dataset.csv` introuvable** :
  - Assurez-vous que `data/healthcare_dataset.csv` existe à la racine du projet.
  - Vérifiez que le chemin dans `src/main.py` (`BASE_DIR / "data" / "healthcare_dataset.csv"`) est correct.
- **Problème : Erreurs dans les tests** :
  - Vérifiez que `poetry.lock` est à jour dans le conteneur :
    ```bash
    docker compose run mongo-mig poetry lock --no-update
    ```
  - Confirmez que `mongomock`, `pytest`, et `pytest-mock` sont installés dans l’image Docker (`poetry show`).
  - Vérifiez les logs des tests pour identifier l’erreur spécifique.
- **Problème : Poetry non installé pour exécution hors Docker** :
  - Installez Poetry avec :
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
  - Puis exécutez `poetry install` à la racine du projet.

Pour plus d’aide, contactez l’auteur.