import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


VALID_EXPERIMENT = {
    "model_name": "Random Forest",
    "dataset": "Breast Cancer Wisconsin",
    "parameters": {
        "n_estimators": 100,
        "max_depth": 8,
    },
    "accuracy": 0.956,
    "f1_score": 0.948,
}


@pytest.fixture
def client(tmp_path):
    database.DATABASE_PATH = tmp_path / "test_experiments.db"

    with TestClient(app) as test_client:
        yield test_client


def test_create_experiment(client):
    response = client.post(
        "/experiments",
        json=VALID_EXPERIMENT,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["model_name"] == "Random Forest"
    assert data["accuracy"] == 0.956


def test_reject_invalid_accuracy(client):
    invalid_experiment = VALID_EXPERIMENT.copy()
    invalid_experiment["accuracy"] = 1.5

    response = client.post(
        "/experiments",
        json=invalid_experiment,
    )

    assert response.status_code == 422


def test_get_all_experiments(client):
    client.post("/experiments", json=VALID_EXPERIMENT)

    response = client.get("/experiments")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_experiment_by_id(client):
    created = client.post(
        "/experiments",
        json=VALID_EXPERIMENT,
    ).json()

    response = client.get(
        f"/experiments/{created['id']}"
    )

    assert response.status_code == 200
    assert response.json()["model_name"] == "Random Forest"


def test_get_best_experiment(client):
    first_experiment = VALID_EXPERIMENT.copy()

    second_experiment = {
        "model_name": "Support Vector Machine",
        "dataset": "Breast Cancer Wisconsin",
        "parameters": {
            "kernel": "rbf",
            "C": 1.0,
        },
        "accuracy": 0.972,
        "f1_score": 0.969,
    }

    client.post("/experiments", json=first_experiment)
    client.post("/experiments", json=second_experiment)

    response = client.get(
        "/experiments/best?metric=accuracy"
    )

    assert response.status_code == 200
    assert response.json()["model_name"] == (
        "Support Vector Machine"
    )


def test_delete_experiment(client):
    created = client.post(
        "/experiments",
        json=VALID_EXPERIMENT,
    ).json()

    experiment_id = created["id"]

    delete_response = client.delete(
        f"/experiments/{experiment_id}"
    )

    get_response = client.get(
        f"/experiments/{experiment_id}"
    )

    assert delete_response.status_code == 204
    assert get_response.status_code == 404