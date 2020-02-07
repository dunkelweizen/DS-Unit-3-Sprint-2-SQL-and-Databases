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

print(collection.count_documents({'Survived': 1}))
print(collection.count_documents({'Survived': 0, 'Pclass': 3}))
average = collection.aggregate([
    {
        "$group":
            {
                "_id": "$Pclass",
                "avgFare": {"$avg": "$Fare"}, }, }
])
for result_object in average:
    print(result_object)

average = collection.aggregate([
    {
        "$group":
            {
                "_id": "$Survived",
                "avgFare": {"$avg": "$Fare"}, }, }
])
for result_object in average:
    print(result_object)

dup_name = collection.aggregate([
    {"$group": {
        "_id": {"Name": "$Name"},
        "uniqueIds": {"$addToSet": "$_id"},
        "count": {"$sum": 1}
        }
    },
    {"$match": {
        "count": {"$gt": 1}
        }
    }
]);
for result_object in dup_name:
    print(result_object)