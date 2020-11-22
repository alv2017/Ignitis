import os

# SETTINGS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR_NAME = "data"
DATA_DIR = os.path.join(ROOT_DIR, DATA_DIR_NAME)

DB_DIR_NAME = "db"
DB_FILE_NAME = "hourly_prices.db"
DB_DIR = os.path.join(ROOT_DIR, DB_DIR_NAME)
DB_FILE = os.path.join(ROOT_DIR, DB_DIR_NAME, DB_FILE_NAME)
