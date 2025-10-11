
from src.utils.envconf import get_vars
from src.pipelines.process_data import process_data
from src.pipelines.migrate_data import migrate_data

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "healthcare_dataset.csv"

def main():
    # Data processing
    hc_data = process_data(str(DATA_PATH))

    # Data migration
    migrate_data(
        hc_data,
        get_vars()['mongo_host'],
        get_vars()['mongo_port'],
        get_vars()['mongo_db'],
        get_vars()['mongo_col'],
        get_vars()['mongo_user'],
        get_vars()['mongo_password']
    )


if __name__ == '__main__':
    main()