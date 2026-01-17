
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import timedelta
from typing import List

from .models import (
    Task, TaskRead, TaskCreate, TaskUpdate,
    User, UserRead, UserCreate, Token
)
from .database import get_session, create_db_and_tables, engine
from .auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from sqlmodel import SQLModel

# Create app
app = FastAPI(
    title="Phase-2 Todo Backend",
    description="Todo app with JWT authentication and PostgreSQL/Neon database",
    version="2.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Backend running", "version": "2.0.0"}


# ============ AUTHENTICATION ENDPOINTS ============

@app.post("/auth/register", response_model=UserRead, tags=["Auth"])
def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user exists
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=Token, tags=["Auth"])
def login(email: str, password: str, session: Session = Depends(get_session)):
    """Login user and return JWT token"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "full_name": user.full_name},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# ============ TASK ENDPOINTS ============

@app.get("/tasks", response_model=List[TaskRead], tags=["Tasks"])
def get_tasks(
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for current user"""
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks


@app.post("/tasks", response_model=TaskRead, tags=["Tasks"])
def create_task(
    task: TaskCreate,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task"""
    db_task = Task(**task.dict(), user_id=current_user.id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def get_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task"""
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return task


@app.put("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task"""
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task"""
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}


# ============ USER ENDPOINTS ============

@app.get("/users/me", response_model=UserRead, tags=["Users"])
def get_current_user_info(
    current_user: UserRead = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@app.put("/users/me", response_model=UserRead, tags=["Users"])
def update_user_profile(
    user_update: dict,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update current user profile"""
    user = session.get(User, current_user.id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "email" in user_update:
        user.email = user_update["email"]
    if "full_name" in user_update:
        user.full_name = user_update["full_name"]
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


