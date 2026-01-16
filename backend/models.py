from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    """Task model for todo application"""
    id: int
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    """Task creation request model"""
    title: str


class TaskUpdate(BaseModel):
    """Task update request model"""
    title: Optional[str] = None
    completed: Optional[bool] = None
