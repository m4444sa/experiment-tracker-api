#database connection and table creation
# import sqlite3
from pathlib import Path

#in sqlite, the database can fit into this one file
DATABASE_PATH = Path("experiments.db")


def get_connection() -> sqlite3.Connection: #reusable connection logic
    connection = sqlite3.connect( #opening database
        DATABASE_PATH,
        check_same_thread=False, #each endpoint opens its own connection
    )
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None: # prepares the table 
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            dataset TEXT NOT NULL,
            parameters TEXT NOT NULL,
            accuracy REAL NOT NULL,
            f1_score REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()