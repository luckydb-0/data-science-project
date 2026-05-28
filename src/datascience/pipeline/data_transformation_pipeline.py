from pathlib import Path

from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_transformation import DataTransformation
from src.datascience import logger

STAGE_NAME = 'Data Transformation Stage'

class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f: # Note: maybe I should read it from the config file?
                status = f.read().split(":")[-1].strip()

            if status == "True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_splitting()
            else:
                raise Exception("Data validation failed. Data transformation was not started.")

        except Exception as e:
            raise e
