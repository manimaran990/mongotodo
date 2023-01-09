from pymongo import MongoClient
import os, urllib

DB_SERVER = os.getenv("MONGO_SERV")
DB_USERNAME = urllib.parse.quote(os.getenv("DB_USERNAME"))
DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))

client = MongoClient(
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/?retryWrites=true&w=majority"
)

db = client["todoDB"]
tasks = db["todos"]