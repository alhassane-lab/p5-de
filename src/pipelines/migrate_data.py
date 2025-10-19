import pandas as pd


def migrate_data(
        df: pd.DataFrame,
        client,
        mongo_db: str,
        mongo_collection: str,
) -> None:
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Convertir en liste de dicts et insérer
    records = df.to_dict('records')
    collection.insert_many(records)

    print(f"{len(records)} documents insérés")