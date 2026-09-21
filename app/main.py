import json
import sqlite3
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Response, status

from app.database import get_connection, init_db
from app.schemas import ExperimentCreate, ExperimentResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="ML Experiment Tracker API",
    description=(
        "A REST API for storing and comparing machine-learning experiments."
    ),
    version="1.0.0",
    lifespan=lifespan,
) # creating the api application


def row_to_experiment(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "model_name": row["model_name"],
        "dataset": row["dataset"],
        "parameters": json.loads(row["parameters"]),
        "accuracy": row["accuracy"],
        "f1_score": row["f1_score"],
        "created_at": row["created_at"],
    } #converting row object into a dict, fastapi does serialization into JSON 


@app.get("/")
def home():
    return {
        "message": "ML Experiment Tracker API",
        "documentation": "/docs",
    }

#decorator to connect urls to functions
@app.post(
    "/experiments",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(experiment: ExperimentCreate):
    connection = get_connection()

    cursor = connection.execute(
        # ? are placeholders, protecting against sql injection
        """
        INSERT INTO experiments (
            model_name,
            dataset,
            parameters,
            accuracy,
            f1_score
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            experiment.model_name,
            experiment.dataset,
            json.dumps(experiment.parameters),
            experiment.accuracy,
            experiment.f1_score,
        ),
    )

    connection.commit()
    #selecting one row
    row = connection.execute(
        "SELECT * FROM experiments WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()

    connection.close()

    return row_to_experiment(row)


@app.get(
    "/experiments",
    response_model=list[ExperimentResponse],
)
def get_experiments():
    connection = get_connection()

    #selecting all rows
    rows = connection.execute(
        "SELECT * FROM experiments ORDER BY id DESC" #sorting desc so recent experiments come first
    ).fetchall()

    connection.close()

    return [row_to_experiment(row) for row in rows]


# this route must appear before /experiments/{experiment_id}.
@app.get(
    "/experiments/best",
    response_model=ExperimentResponse,
)
def get_best_experiment(
    metric: Literal["accuracy", "f1_score"] = "accuracy",
):
    connection = get_connection()

    # The Literal validation ensures only these two columns can be used.
    metric_column = {
        "accuracy": "accuracy",
        "f1_score": "f1_score",
    }[metric]

    row = connection.execute(
        f"""
        SELECT *
        FROM experiments
        ORDER BY {metric_column} DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="No experiments have been recorded",
        )

    return row_to_experiment(row)


@app.get(
    "/experiments/{experiment_id}",
    response_model=ExperimentResponse,
)
def get_experiment(experiment_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM experiments WHERE id = ?",
        (experiment_id,),
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found",
        )

    return row_to_experiment(row)


@app.delete(
    "/experiments/{experiment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experiment(experiment_id: int):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM experiments WHERE id = ?",
        (experiment_id,),
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)