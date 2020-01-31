import json
import os
from dotenv import load_dotenv
import pandas as pd
import sqlite3
import psycopg2
from psycopg2.extras import execute_values

data = pd.read_csv('titanic.csv')

conn = sqlite3.connect("titanic.sqlite3")
data.to_sql('passengers', conn, if_exists='replace')
curs = conn.cursor()

load_dotenv()  # looks inside the .env file for some env vars

# passes env var values to python var
DB_HOST = os.getenv("DB_HOST", default="OOPS")
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")

DB_FILEPATH = "titanic.sqlite3"


class StorageService():
    def __init__(self):
        self.sqlite_connection = sqlite3.connect(DB_FILEPATH)
        self.sqlite_cursor = self.sqlite_connection.cursor()
        self.pg_connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        self.pg_cursor = self.pg_connection.cursor()

    def get_passengers(self):
        return self.sqlite_connection.execute("SELECT * FROM passengers;").fetchall()

    def create_passengers_table(self):
        create_query = """
        DROP TABLE IF EXISTS passengers; -- allows this to be run idempotently, avoids psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "characters_pkey" DETAIL:  Key (character_id)=(1) already exists.
        CREATE TABLE IF NOT EXISTS passengers (
            index SERIAL PRIMARY KEY,
            Survived INT,
            Pclass INT,
            Name VARCHAR(255),
            Sex VARCHAR(6),
            Age INT,
            SiblingsSpousesAboard INT,
            ParentsChildrenAboard INT,
            Fare REAL
        );
        """
        print(create_query)
        self.pg_cursor.execute(create_query)
        self.pg_connection.commit()

    def insert_passengers(self, passengers):
        insertion_query = "INSERT INTO passengers (index, Survived, Pclass, Name, " \
                          "Sex, Age, SiblingsSpousesAboard, ParentsChildrenAboard, Fare) VALUES %s"
        list_of_tuples = passengers
        execute_values(self.pg_cursor, insertion_query, list_of_tuples)
        self.pg_connection.commit()


if __name__ == "__main__":
    service = StorageService()

    #
    # EXTRACT AND TRANSFORM
    #

    passengers = service.get_passengers()

    #
    # LOAD
    #

    service.create_passengers_table()

    service.insert_passengers(passengers)
