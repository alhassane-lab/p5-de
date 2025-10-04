import pandas as pd
from pymongo import MongoClient
import os








def migrate_to_mongo(
        df: pd.DataFrame,
        mongo_host,
        mongo_port,
        mongo_database,
        mongo_collection
) -> None:

    # Connexion à MongoDB (utilise des variables d'env pour la sécurité)
    client = MongoClient(f"{mongo_host}://localhost:{mongo_port}/")
    db = client[mongo_database]
    collection = db[mongo_collection]

    # Convertir en liste de dicts et insérer
    records = df.to_dict('records')
    collection.insert_many(records)
    print(f"{len(records)} documents insérés avec succès.")