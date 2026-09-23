import time

import requests
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


API_URL = "http://127.0.0.1:8000/experiments"


def train_model():
    #  load a real classification dataset
    dataset = load_breast_cancer()

    X = dataset.data
    y = dataset.target

    # divide the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # define the experiment parameters
    parameters = {
        "n_estimators": 100,
        "max_depth": 8,
        "random_state": 42,
    }

    #create the model
    model = RandomForestClassifier(**parameters)

    # measure training duration
    start_time = time.perf_counter()

    model.fit(X_train, y_train)

    training_time = time.perf_counter() - start_time

    # make predictions
    predictions = model.predict(X_test)

    # calculate evaluation metrics
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    return parameters, accuracy, f1, training_time


def log_experiment(parameters, accuracy, f1, training_time):
    # create data matching ExperimentCreate
    experiment = {
        "model_name": "Random Forest",
        "dataset": "Breast Cancer Wisconsin",
        "parameters": {
            **parameters,
            "training_time_seconds": round(training_time, 4),
        },
        "accuracy": float(accuracy),
        "f1_score": float(f1),
    }

    # 9. send the results to your API
    response = requests.post(
        API_URL,
        json=experiment,
        timeout=10,
    )

    # raise an error if the API request failed
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    parameters, accuracy, f1, training_time = train_model()

    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 score: {f1:.4f}")
    print(f"Training time: {training_time:.4f} seconds")

    saved_experiment = log_experiment(
        parameters,
        accuracy,
        f1,
        training_time,
    )

    print("\nExperiment saved successfully:")
    print(saved_experiment)