import pandas as pd
from pymongo import MongoClient




def migrate_data(
        df: pd.DataFrame,
        mongo_host: str,
        mongo_port: str,
        mongo_database: str,
        mongo_collection: str
) -> None:

    # Connexion à MongoDB
    #client = MongoClient(f"{mongo_host}://root:password@mongo:{mongo_port}/")
    client = MongoClient(f"{mongo_host}://mongo:{mongo_port}/")
    db = client[mongo_database]
    collection = db[mongo_collection]

    # Convertir en liste de dicts et insérer
    records = df.to_dict('records')
    collection.insert_many(records)

    print(f"{len(records)} documents insérés avec succès.")