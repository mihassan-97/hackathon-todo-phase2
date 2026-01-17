from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
import os

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://user:password@localhost:5432/todo_db"
)

# Create engine with appropriate settings for async
connect_args = {}
if DATABASE_URL.startswith("postgresql"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
    poolclass=NullPool if "postgres" in DATABASE_URL else None,
)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
