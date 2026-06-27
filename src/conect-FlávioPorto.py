import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def connect() -> mysql.connector.connection.MySQLConnection:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "intelliwrite"),
    )
    return connection

def initialize_database(schema_path: str = "schema_ava.sql") -> None:
    schema_file = Path(schema_path)
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema não encontrado: {schema_path}")

    # Connect without database to create it if it doesn't exist
    conn_no_db = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
    )
    cursor_no_db = conn_no_db.cursor()
    db_name = os.getenv("MYSQL_DATABASE", "intelliwrite")
    cursor_no_db.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn_no_db.close()

    # Now connect with the database to run the schema
    connection = connect()
    cursor = connection.cursor()
    
    # Read the schema file and execute statement by statement
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Erro ao executar: {command}\n{e}")
    
    connection.commit()
    connection.close()
