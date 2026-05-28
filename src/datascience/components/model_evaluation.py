import os
from pathlib import Path
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from src.datascience import logger
from src.datascience.entity.config_entity import ModelEvaluationConfig
from src.datascience.utils.common import save_json
from src.datascience.utils.common import *
from src.datascience.constants import *


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self):
        mlflow_password = os.getenv("MLFLOW_TRACKING_PASSWORD")

        if not mlflow_password:
            raise ValueError(
                "MLFLOW_TRACKING_PASSWORD is not set. "
                "Please export it locally before running model evaluation."
            )
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis = 1)
        test_y = test_data[[self.config.target_column]]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            predicted_qualities = model.predict(test_x)

            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
            
            # Saving metrics as local
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path = Path(self.config.metric_file_name), data = scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # Register the model if the tracking server supports it.
            # If registry creation fails, fall back to a plain model log.
            if tracking_url_type_store != "file":
                try:
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticnetModel")
                except Exception as e:
                    logger.warning(
                        "Model registry unavailable or not permitted; logging model without registration."
                        f" Error: {e}"
                    )
                    mlflow.sklearn.log_model(model, "model")
            else:
                mlflow.sklearn.log_model(model, "model")