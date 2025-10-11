import pandas as pd
from pymongo import MongoClient




def migrate_data(
        df: pd.DataFrame,
        mongo_host: str,
        mongo_port: str,
        mongo_db: str,
        mongo_collection: str,
        mongo_user: str,
        mongo_password: str
) -> None:

    # Connexion à MongoDB
    #client = MongoClient(f"{mongo_host}://root:password@mongo:{mongo_port}/")
    #   mongo_uri = "mongodb://root:password@mongo:27017/admin"
    #client = MongoClient(f"{mongo_host}://mongo:{mongo_port}/")
    mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource={mongo_db}"
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Convertir en liste de dicts et insérer
    records = df.to_dict('records')
    collection.insert_many(records)

    print(f"{len(records)} documents insérés avec succès.")