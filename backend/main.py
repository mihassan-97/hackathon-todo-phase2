from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import Task, TaskCreate, TaskUpdate
from typing import List

app = FastAPI(title="Todo API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
tasks_db: dict[int, Task] = {}
task_id_counter = 1


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Todo API is running"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """Create a new task"""
    global task_id_counter
    
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        completed=False
    )
    tasks_db[task_id_counter] = new_task
    task_id_counter += 1
    
    return new_task


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def get_all_tasks():
    """Retrieve all tasks"""
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: int):
    """Retrieve a specific task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return tasks_db[task_id]


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    existing_task = tasks_db[task_id]
    
    if task_update.title is not None:
        existing_task.title = task_update.title
    if task_update.completed is not None:
        existing_task.completed = task_update.completed
    
    return existing_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: int):
    """Delete a task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    del tasks_db[task_id]
    return None


@app.delete("/tasks", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_all_tasks():
    """Delete all tasks"""
    tasks_db.clear()
    return None
