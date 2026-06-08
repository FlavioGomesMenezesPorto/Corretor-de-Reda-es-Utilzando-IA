import sqlite3
from pathlib import Path


def connect(database_path: str = "IA.db") -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize_database(database_path: str = "IA.db", schema_path: str = "schema_ava.sql") -> None:
    schema_file = Path(schema_path)
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema não encontrado: {schema_path}")

    with connect(database_path) as connection:
        connection.executescript(schema_file.read_text(encoding="utf-8"))
