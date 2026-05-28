# End-to-End Data Science Project

This repository is a beginner-friendly MLOps bootcamp exercise for building an end-to-end machine learning pipeline around the red wine quality dataset.

The project downloads the dataset, validates its schema, creates train/test splits, trains an ElasticNet regression model, evaluates it with **MLflow/DagsHub** tracking, and exposes a simple **Flask** form for predictions.

## Project Overview

The current pipeline predicts the `quality` target column from physicochemical wine measurements such as acidity, chlorides, density, pH, sulphates, and alcohol.

The implementation follows a staged pipeline structure:

1. Data ingestion
2. Data validation
3. Data transformation
4. Model training
5. Model evaluation
6. Prediction through a Flask web app

Runtime outputs such as downloaded data, trained models, metrics, and logs are written under ignored folders like `artifacts/` and `logs/`.

## Tech Stack

- Python
- pandas and NumPy
- scikit-learn
- DagsHub/MLflow tracking
- Flask
- PyYAML and python-box
- joblib

## Repository Structure

```text
data-science-project/
├── config/
│   └── config.yaml                  # Pipeline paths and data source configuration
├── research/                        # Experiment notebooks for individual stages
├── src/
│   └── datascience/
│       ├── components/              # Stage implementation logic
│       ├── config/                  # Configuration manager
│       ├── constants/               # Config paths and MLflow environment defaults
│       ├── entity/                  # Dataclass-based configuration entities
│       ├── pipeline/                # Stage orchestration classes
│       └── utils/                   # Shared helpers for YAML, JSON, directories, binaries
├── templates/                       # Flask HTML templates
├── app.py                           # Flask application for training and prediction
├── main.py                          # Runs the full training/evaluation pipeline
├── params.yaml                      # Model hyperparameters
├── schema.yaml                      # Expected dataset schema and target column
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Present but currently empty
├── setup.py                         # Present but currently empty
└── README.md
```

## Configuration Files

### `config/config.yaml`

Defines the pipeline artifact root and paths for each stage.

Important values include:

- `artifacts_root`: base folder for generated pipeline outputs.
- `data_ingestion.source_URL`: remote ZIP file containing `winequality-red.csv`.
- `data_validation.unzip_data_dir`: extracted CSV path used for validation.
- `data_transformation.data_path`: CSV input used to create train/test splits.
- `model_trainer.model_name`: saved model filename, currently `model.joblib`.
- `model_evaluation.metric_file_name`: local JSON metrics output path.

### `params.yaml`

Stores ElasticNet hyperparameters:

```yaml
ElasticNet:
  alpha: 0.2
  l1_ratio: 0.1
```

### `schema.yaml`

Defines the expected input columns, their pandas dtypes, and the target column:

- Target column: `quality`
- Feature columns: wine chemistry measurements such as `fixed acidity`, `volatile acidity`, `citric acid`, `residual sugar`, `chlorides`, `density`, `pH`, `sulphates`, and `alcohol`.

The data validation stage checks that the dataset columns exactly match this schema and that the dtypes match the expected values.

## Installation

From the repository root:

```bash
python -m venv .venv-ds
source .venv-ds/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with:

```bash
.venv-ds\Scripts\activate
```

## MLflow and DagsHub Setup

The project is configured to use DagsHub as the MLflow tracking server.

The current MLflow defaults are set in `src/datascience/constants/__init__.py`:

```python
MLFLOW_TRACKING_URI = "https://dagshub.com/luckydb-0/data-science-project.mlflow"
MLFLOW_TRACKING_USERNAME = "luckydb-0"
```

The password/token is intentionally expected from the local environment. Before running the full pipeline, export your DagsHub MLflow password or token:

```bash
export MLFLOW_TRACKING_PASSWORD="your-dagshub-token"
```

Without `MLFLOW_TRACKING_PASSWORD`, the model evaluation stage raises an error and the full `main.py` pipeline will stop at evaluation.

## Usage

### Run the Full Pipeline

After installing dependencies and setting the MLflow password:

```bash
python main.py
```

This runs the stages in order:

1. Downloads the wine quality ZIP file.
2. Extracts `winequality-red.csv`.
3. Validates columns and dtypes against `schema.yaml`.
4. Splits the dataset into `train.csv` and `test.csv`.
5. Trains an ElasticNet model.
6. Saves the model as `artifacts/model_trainer/model.joblib`.
7. Evaluates the model with RMSE, MAE, and R2.
8. Saves metrics to `artifacts/model_evaluation/metrics.json`.
9. Logs parameters, metrics, and the model to MLflow.

### Run the Flask App

The Flask app serves a simple form for entering wine feature values and getting a predicted quality score.

Start the app with:

```bash
python app.py
```

Then open:

```text
http://localhost:8080
```

Available routes:

- `/`: renders the input form.
- `/predict`: accepts form input and returns a prediction.
- `/train`: runs `main.py` from the web app.

Important: prediction requires the trained model file at `artifacts/model_trainer/model.joblib`. Run the training pipeline first.

## ML Pipeline Stages

### 1. Data Ingestion

Implemented in `src/datascience/components/data_ingestion.py`.

This stage downloads the configured ZIP file from GitHub and extracts it into the data ingestion artifact directory.

Output:

- `artifacts/data_ingestion/data.zip`
- `artifacts/data_ingestion/winequality-red.csv`

### 2. Data Validation

Implemented in `src/datascience/components/data_validation.py`.

This stage reads the extracted CSV and validates:

- the set of columns against `schema.yaml`
- each column dtype against `schema.yaml`

Output:

- `artifacts/data_validation/status.txt`

### 3. Data Transformation

Implemented in `src/datascience/components/data_transformation.py`.

This stage currently performs a train/test split. No scaling, encoding, PCA, or other preprocessing is applied in the current code.

Output:

- `artifacts/data_transformation/train.csv`
- `artifacts/data_transformation/test.csv`

### 4. Model Training

Implemented in `src/datascience/components/model_trainer.py`.

This stage trains a scikit-learn `ElasticNet` regression model using the hyperparameters from `params.yaml`.

Output:

- `artifacts/model_trainer/model.joblib`

### 5. Model Evaluation

Implemented in `src/datascience/components/model_evaluation.py`.

This stage loads the trained model, predicts on the test set, calculates regression metrics, saves them locally, and logs the run to MLflow.

Metrics:

- RMSE
- MAE
- R2

Output:

- `artifacts/model_evaluation/metrics.json`
- MLflow run with parameters, metrics, and model artifact

When the tracking URI is not a local file store, the code attempts to register the model as `ElasticnetModel`. If registry registration is unavailable or not permitted, it falls back to logging the model without registration.

## Development Workflow

The repository follows a common staged MLOps workflow:

1. Update `config/config.yaml` for paths and stage settings.
2. Update `schema.yaml` when the dataset schema changes.
3. Update `params.yaml` for model hyperparameters.
4. Update configuration entities in `src/datascience/entity/config_entity.py`.
5. Update the configuration manager in `src/datascience/config/configuration.py`.
6. Update stage components in `src/datascience/components/`.
7. Update pipeline orchestration in `src/datascience/pipeline/`.
8. Update `main.py` if the stage order changes.

## Notes and Current Limitations

- `Dockerfile` and `setup.py` are present but currently empty.
- There are no automated tests.
- The train/test split does not currently set `test_size`, `random_state`, or stratification.
- The Flask form expects all inputs to be numeric and does not include advanced validation.
- `templates/index.html` references a background image under `static/assets/img/form-v9.jpg`, but no `static/` folder is present in the repository.
- Full pipeline execution depends on DagsHub MLflow credentials because evaluation logs to the configured remote tracking server.

## Future Improvements

Possible improvements based on the current project state:

- Add automated tests for configuration loading, validation, training, and prediction.
- Make MLflow tracking URI, username, and password fully environment-driven.
- Complete the `Dockerfile` for reproducible containerized execution.
- Complete `setup.py` or replace it with a modern packaging configuration.
- Add a CI workflow under `.github/workflows/`.
- Add a deterministic train/test split by setting `random_state` and `test_size`.
- Add preprocessing through a scikit-learn pipeline if future models require scaling or feature engineering.
- Improve Flask input validation and error messages.
- Add example input values for manual prediction testing.

## License

This repository includes an Apache License 2.0 file.
