import os
from src.datascience import logger
import pandas as pd

from src.datascience.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            data = pd.read_csv(self.config.unzip_data_dir)

            schema = self.config.all_schema

            data_columns = set(data.columns)
            schema_columns = set(schema.keys())

            validation_status = True

            # Check that columns are exactly the same
            if data_columns != schema_columns:
                validation_status = False
            else:
                # Check column data types
                for col, expected_dtype in schema.items():
                    actual_dtype = str(data[col].dtype)

                    if actual_dtype != expected_dtype:
                        validation_status = False
                        break

            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e