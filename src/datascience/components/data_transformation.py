import os
from src.datascience.entity.config_entity import DataTransformationConfig
from src.datascience import logger
from sklearn.model_selection import train_test_split
import pandas as pd

class DataTransformation:
    # Note: This is an example of data transformation. Only train test splitting is applied but here you could
    # do any transformation technique such as Scaler, PCA, etc...
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_splitting(self):
        data = pd.read_csv(self.config.data_path)

        train, test = train_test_split(data)

        train.to_csv(os.path.join(self.config.root_dir, 'train.csv'), index = False)
        test.to_csv(os.path.join(self.config.root_dir, 'test.csv'), index = False)

        logger.info('Splitted data into training and test sets.')
        logger.info(f'Train shape: {train.shape}')
        logger.info(f'Test shape: {test.shape}')