from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from app.models.task import Task
from app.db import tasks


router = APIRouter()

@router.post("/tasks")
async def create_task(task: Task):
    """ create a new task """
    try:
        task_id = tasks.insert_one(task.dict()).inserted_id
        return {"success": True, "id": str(task_id)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/tasks/")
async def get_tasks(
    id: str = Query(None, description="task id"),
    date: str = Query(None, description="query date in regex. ex. yyyy-mm-dd")
    ):
    """ get all task(s) by a id or date(regex) """
    all_tasks = {}
    try:
        if id:
            task_list = tasks.find_one({"_id": ObjectId(id)})
            all_tasks = task_list
        elif date:
            task_list = tasks.find({"due_date": {"$regex": date}})
            all_tasks = list(task_list)
        return {"success":True, "tasks": all_tasks }
        # content = {"success":True, "tasks": all_tasks }
        # return Response(status_code=201, content=content)
    except Exception as e:
        return {"success": False, "error": str(e)}
        # return Response(status_code=400, content={"error":str(e)})

@router.patch("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    """ update a task """
    try:
        task_id = ObjectId(task_id)
        result = tasks.update_one({"_id": task_id}, {"$set": task.dict()})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """delete a task"""
    try:
        task_id = ObjectId(task_id)
        result = tasks.delete_one({"_id": task_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}