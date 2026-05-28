from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationPipeline
from src.datascience.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.datascience.pipeline.model_trainer_pipeline import ModelTrainingPipeline
from src.datascience.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline


STAGE_NAME = 'Data Ingestion Stage'
try:
    logger.info(f'>>>>> stage {STAGE_NAME} started <<<<<')
    obj = DataIngestionPipeline()
    obj.initiate_data_ingestion()
    logger.info(f'>>>>> stage {STAGE_NAME} completed <<<<<\n')
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = 'Data Validation Stage'
try:
    logger.info(f'>>>>> stage {STAGE_NAME} started <<<<<')
    obj = DataValidationPipeline()
    obj.initiate_data_validation()
    logger.info(f'>>>>> stage {STAGE_NAME} completed <<<<<\n')
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = 'Data Transformation Stage'
try:
    logger.info(f'>>>>> stage {STAGE_NAME} started <<<<<')
    obj = DataTransformationPipeline()
    obj.initiate_data_transformation()
    logger.info(f'>>>>> stage {STAGE_NAME} completed <<<<<\n')
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = 'Model Training Stage'
try:
    logger.info(f'>>>>> stage {STAGE_NAME} started <<<<<')
    obj = ModelTrainingPipeline()
    obj.initiate_model_training()
    logger.info(f'>>>>> stage {STAGE_NAME} completed <<<<<\n')
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = 'Model Evaluation Stage'
try:
    logger.info(f'>>>>> stage {STAGE_NAME} started <<<<<')
    obj = ModelEvaluationPipeline()
    obj.model_evaluation()
    logger.info(f'>>>>> stage {STAGE_NAME} completed <<<<<\n')
except Exception as e:
    logger.exception(e)
    raise e