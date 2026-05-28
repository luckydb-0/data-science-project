from src.datascience.components.model_evaluation import ModelEvaluation
from src.datascience.config.configuration import ConfigurationManager

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def model_evaluation(self):
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config = model_evaluation_config)
            model_evaluation.log_into_mlflow()