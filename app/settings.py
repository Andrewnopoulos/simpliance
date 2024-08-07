import os

results_path_default = 'results'
db_path_default = 'test.db'
db_setup_file_default = 'db_setup.sql'

RESULTS_PATH =  os.environ.get("RESULTS_PATH", results_path_default)
DB_PATH =       os.environ.get("DB_PATH", db_path_default)
DB_SETUP_FILE = os.environ.get("DB_SETUP_FILE", db_setup_file_default)