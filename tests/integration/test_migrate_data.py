import pytest
import pandas as pd
import mongomock
from src.pipelines.migrate_data import migrate_data

# Données simulées via un dictionnaire
DATA = {
    "name": ["John Doe", "Jane Smith", "Alice Brown"],
    "age": [30, 40, 25],
    "patient_id": [1, 2, 3]
}

@pytest.fixture
def sample_df():
    """Crée un DataFrame à partir des données simulées"""
    return pd.DataFrame(DATA)

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
    collection.drop()
    yield collection
    collection.drop()

def test_migrate_data(sample_df, mongo_client, db_collection):
    """Test d'intégration simple pour migrate_data"""
    # Appeler migrate_data
    migrate_data(
        df=sample_df,
        client=mongo_client,
        mongo_db="healthcare",
        mongo_collection="patients"
    )

    # Vérifier le nombre de documents insérés
    count = db_collection.count_documents({})
    assert count == 3, f"Attendu 3 documents, trouvé {count}"

    # Vérifier le contenu des documents insérés
    docs = list(db_collection.find({}))

    assert len(docs) == 3
    print(f"nombre de documents dans find() attendu 3, trouvé {len(docs)}")

    assert docs[0]["name"] == "John Doe"
    print(f"name attendu 'John Doe', trouvé {docs[0]['name']}")

    assert docs[0]["age"] == 30
    print(f"age attendu 30, trouvé {docs[0]['age']}")

    assert docs[0]["patient_id"] == 1
    print(f"patient_id attendu 1, trouvé {docs[0]['patient_id']}")

    assert docs[1]["name"] == "Jane Smith"
    print(f"Attendu 'Jane Smith', trouvé {docs[1]['name']}")

    assert docs[1]["age"] == 40
    print(f"age attendu 40, trouvé {docs[1]['age']}")

    assert docs[1]["patient_id"] == 2
    print(f"patient_id attendu 2, trouvé {docs[1]['patient_id']}")

    assert docs[2]["name"] == "Alice Brown"
    print(f"name attendu 'Alice Brown', trouvé {docs[2]['name']}")

    assert docs[2]["age"] == 25
    print(f"age attendu 25, trouvé {docs[2]['age']}")

    assert docs[2]["patient_id"] == 3
    print(f"patient_id attendu 3, trouvé {docs[2]['patient_id']}")