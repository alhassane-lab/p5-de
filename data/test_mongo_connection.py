import pytest
import mongomock
from src.pipelines.migrate_data import migrate_data
import pandas as pd


@pytest.fixture
def mongo_client():
    """Fixture pour un client MongoDB simulé avec mongomock"""
    client = mongomock.MongoClient()
    yield client
    client.close()


@pytest.fixture
def db_collection(mongo_client):
    """Fixture pour une collection vide dans la base healthcare"""
    db = mongo_client["healthcare"]
    collection = db["patients"]
    collection.drop()  # Nettoie avant le test
    yield collection
    collection.drop()  # Nettoie après le test


def test_migrate_data_inserts_correctly(db_collection, mongo_client):
    """Teste que migrate_data insère les enregistrements correctement"""
    sample_records = [
        {"name": "Patient1", "age": 30, "id": "1"},
        {"name": "Patient2", "age": 40, "id": "2"}
    ]

    # Simule l'environnement attendu par migrate_data
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("MONGO_DB", "healthcare")
        mp.setenv("MONGO_COLLECTION", "patients")

        # Appelle la fonction
        migrate_data(pd.DataFrame(sample_records))

    # Vérifie le contenu de la collection
    count = db_collection.count_documents({})
    assert count == 2, f"Attendu 2 documents, trouvé {count}"

    docs = list(db_collection.find({}))
    assert len(docs) == 2
    assert docs[0]["name"] == "Patient1"
    assert docs[0]["age"] == 30
    assert docs[1]["name"] == "Patient2"
    assert docs[1]["age"] == 40


def test_migrate_data_idempotent(db_collection, mongo_client):
    """Teste que migrate_data est idempotent"""
    sample_records = [
        {"name": "Patient1", "age": 30, "id": "1"}
    ]

    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("MONGO_DB", "healthcare")
        mp.setenv("MONGO_COLLECTION", "patients")

        # Première migration
        migrate_data(records=sample_records)
        # Deuxième migration
        migrate_data(records=sample_records)

    # Vérifie qu'il n'y a pas de duplication
    count = db_collection.count_documents({})
    assert count == 1, f"Attendu 1 document, trouvé {count}"

    doc = db_collection.find_one({"id": "1"})
    assert doc["name"] == "Patient1"
    assert doc["age"] == 30