from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    """Base Task model with common fields"""
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRead(TaskBase):
    """Task read schema"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Task creation schema"""
    pass


class TaskUpdate(SQLModel):
    """Task update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class UserBase(SQLModel):
    """Base User model"""
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None


class User(UserBase, table=True):
    """User table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    """User read schema"""
    id: int
    is_active: bool
    created_at: datetime


class UserCreate(UserBase):
    """User creation schema"""
    password: str


class UserUpdate(SQLModel):
    """User update schema"""
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class Token(SQLModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"

