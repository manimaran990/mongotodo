from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
import datetime
from typing import Optional
import os, urllib


class Task(BaseModel):
    task: str
    description: Optional[str]
    due_date: str = datetime.date.today()
    completed: bool = False

app = FastAPI()

DB_SERVER = os.getenv("MONGO_SERV")
DB_USERNAME = urllib.parse.quote(os.getenv("DB_USERNAME"))
DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))

client = MongoClient(
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/?retryWrites=true&w=majority"
)

db = client["todoDB"]
tasks = db["todos"]


@app.post("/tasks")
async def create_task(task: Task):
    task_id = tasks.insert_one(task.dict()).inserted_id
    return {"id": str(task_id)}


@app.get("/tasks/date")
async def get_tasks(date: str):
    all_tasks = list(tasks.find({"due_date": {"$regex": date}}, {'_id': False}))
    return all_tasks


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    tasks.update_one({"_id": task_id}, {"$set": task.dict()})
    return {"success": True}
