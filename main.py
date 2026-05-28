from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationPipeline
from src.datascience.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.datascience.pipeline.model_trainer_pipeline import ModelTrainingPipeline
from src.datascience.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline

def run_stage(stage_name: str, stage_callable) -> None:
    """
    Run a single pipeline stage with logging and error handling.
    """
    try:
        logger.info(f">>>>> stage {stage_name} started <<<<<")
        stage_callable()
        logger.info(f">>>>> stage {stage_name} completed <<<<<\n")
    except Exception:
        logger.exception(f"Error occurred while running stage: {stage_name}")
        raise

if __name__ == "__main__":
    stages = [
        (
            "Data Ingestion Stage",
            lambda: DataIngestionPipeline().initiate_data_ingestion(),
        ),
        (
            "Data Validation Stage",
            lambda: DataValidationPipeline().initiate_data_validation(),
        ),
        (
            "Data Transformation Stage",
            lambda: DataTransformationPipeline().initiate_data_transformation(),
        ),
        (
            "Model Training Stage",
            lambda: ModelTrainingPipeline().initiate_model_training(),
        ),
        (
            "Model Evaluation Stage",
            lambda: ModelEvaluationPipeline().model_evaluation(),
        ),
    ]

    for stage_name, stage_callable in stages:
        run_stage(stage_name, stage_callable)