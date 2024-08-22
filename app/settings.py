import os

results_path_default = 'results'
db_path_default = 'test.db'
db_setup_file_default = '../db_setup.sql'
aws_access_key_id_default = "missing_aws_key"
aws_secret_access_key_default = "missing_aws_secret"
connection_path_default = 'aws_connections'
credential_path_default = 'aws_credentials'
jwt_encryption_key_default = 'missing_jwt_key'

RESULTS_PATH =          os.environ.get("RESULTS_PATH", results_path_default)
DB_PATH =               os.environ.get("DB_PATH", db_path_default)
DB_SETUP_FILE =         os.environ.get("DB_SETUP_FILE", db_setup_file_default)
AWS_ACCESS_KEY_ID =     os.environ.get("AWS_ACCESS_KEY_ID", aws_access_key_id_default)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", aws_secret_access_key_default)
JWT_ENCRYPTION_KEY =    os.environ.get("JWT_ENCRYPTION_KEY", jwt_encryption_key_default)

CONNECTIONS_PATH = os.environ.get("CONNECTIONS_PATH", connection_path_default)
CREDENTIALS_PATH = os.environ.get("CREDENTIALS_PATH", credential_path_default)