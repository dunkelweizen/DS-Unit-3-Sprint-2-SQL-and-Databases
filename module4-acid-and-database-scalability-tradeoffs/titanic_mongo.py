import pymongo
import os
from dotenv import load_dotenv
import pandas as pd
import sqlite3

load_dotenv()
DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")
connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}-8evf9.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri)
db = client.titanic
collection = db.titanic

conn = sqlite3.connect("titanic.sqlite3")
cursor = conn.cursor()

query = f"SELECT * FROM titanic"
cursor.execute(query)
for i in range(len(cursor.fetchall())):
        cursor.execute(query)
        row = cursor.fetchall()[i]
        keys = [description[0] for description in cursor.description]
        row_dict = dict()
        for j in range(len(keys)):
            row_dict[keys[j]] = row[j]
        collection.insert_one(row_dict)