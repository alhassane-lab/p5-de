"""
Get environment variables from .env
"""
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


def get_vars():
    """
    Post-processing method that creates an instance of EnvConf
    """
    # ! auto activate .env
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    kwargs = {
        'csv_path': os.getenv("CSV_PATH"),
        'mongo_db': os.getenv("MONGO_DB"),
        'mongo_col': os.getenv("MONGO_COLLECTION"),
        'mongo_host': os.getenv("MONGO_HOST"),
        'mongo_port': os.getenv("MONGO_PORT"),
        'mongo_user' : os.getenv("MONGO_APP_USER"),
        'mongo_password' : os.getenv("MONGO_APP_PASSWORD")
    }
    return kwargs

