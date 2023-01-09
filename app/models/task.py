import pydantic
from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId
import datetime
from enum import Enum


from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


class Recurrence(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class Task(BaseModel):
    _id: ObjectId
    task: str
    recurrence: Recurrence
    description: Optional[str]
    due_date: str = datetime.date.today()
    completed: bool = False
