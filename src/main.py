from src.pipelines.migrate_to_mongo import migrate_to_mongo
from src.pipelines.preprocess_data import process_data
import os

mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_database = os.getenv("MONGO_DATABASE")
mongo_collection = os.getenv("MONGO_COLLECTION")


def main():
    process_data()