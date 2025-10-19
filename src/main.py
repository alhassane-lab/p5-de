from pymongo import MongoClient
from src.utils.envconf import get_vars
from src.pipelines.process_data import process_data
from src.pipelines.migrate_data import migrate_data

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "healthcare_dataset.csv"

def get_mongo_client(
            mongo_host: str,
            mongo_port: str,
            mongo_db: str,
            mongo_user: str,
            mongo_password: str
    ) :
    mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource={mongo_db}"
    client = MongoClient(mongo_uri)
    return client


def main():
    # Data processing
    hc_data = process_data(str(DATA_PATH))

    client = get_mongo_client(
        get_vars()['mongo_host'],
        get_vars()['mongo_port'],
        get_vars()['mongo_db'],
        get_vars()['mongo_user'],
        get_vars()['mongo_password']
    )
    # Data migration
    migrate_data(
        hc_data,
        client,
        get_vars()['mongo_db'],
        get_vars()['mongo_col']
    )


if __name__ == '__main__':
    main()