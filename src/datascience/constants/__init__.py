from pathlib import Path
import os

CONFIG_FILEPATH = Path('config/config.yaml')
PARAMS_FILEPATH = Path('params.yaml')
SCHEMA_FILEPATH = Path('schema.yaml')

# These MLFLOW constants must be env variables
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/luckydb-0/data-science-project.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "luckydb-0"
os.environ.setdefault("MLFLOW_TRACKING_PASSWORD", "") # To not overwrite a real local env variable
