# ML Experiment Tracker API

This is a small REST API I built to practice backend development and learn how APIs work with databases.

It can store machine learning experiments with information such as the model name, dataset, parameters, accuracy, and F1 score. You can also retrieve experiments, compare them by a selected metric, and delete them.

The project uses Python, FastAPI, Pydantic, SQLite, and pytest.

## Features

* Save a new experiment
* Retrieve all experiments, or retrieve experiment bz ID
* Find the best experiment by accuracy or F1 score
* Delete an experiment
* Validate input data
* Store data in SQLite
* Test the API through Swagger documentation

## Running the project

Clone the repository and enter the project folder:

```bash
git clone https://github.com/m4444sa/ml-experiment-tracker-api.git
cd ml-experiment-tracker-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install the dependencies:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the API:

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open the Swagger documentation here:

```text
http://127.0.0.1:8000/docs
```

## Example experiment

```json
{
  "model_name": "Random Forest",
  "dataset": "Breast Cancer Wisconsin",
  "parameters": {
    "n_estimators": 100,
    "max_depth": 8
  },
  "accuracy": 0.956,
  "f1_score": 0.948
}
```

## Endpoints

* `POST /experiments` saves an experiment
* `GET /experiments` returns all experiments
* `GET /experiments/{id}` returns one experiment
* `GET /experiments/best?metric=accuracy` finds the best experiment
* `DELETE /experiments/{id}` deletes an experiment

## Tests

Run the tests with:

```bash
.venv\Scripts\python.exe -m pytest -v
```

While building this project, I practiced working with REST APIs, JSON data, input validation, SQL queries, HTTP status codes, SQLite databases, and automated API testing.

## Inspiration

A short introduction to the framework used in this project:

[FastAPI in 15 Minutes - Crash Course for Beginners](https://www.youtube.com/watch?v=BPRKBQwEHe0)



