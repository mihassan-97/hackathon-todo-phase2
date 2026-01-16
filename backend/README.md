# Backend - Todo API (FastAPI)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health Check
- `GET /` - Health check

### Tasks (CRUD Operations)
- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a specific task
- `DELETE /tasks` - Delete all tasks

## Request/Response Format

### Create Task
```json
POST /tasks
{
  "title": "Buy groceries"
}

Response (201):
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

### Get All Tasks
```json
GET /tasks

Response (200):
[
  {
    "id": 1,
    "title": "Buy groceries",
    "completed": false
  }
]
```

### Update Task
```json
PUT /tasks/1
{
  "title": "Buy groceries and cook",
  "completed": true
}

Response (200):
{
  "id": 1,
  "title": "Buy groceries and cook",
  "completed": true
}
```

### Delete Task
```json
DELETE /tasks/1

Response (204): No Content
```

## Architecture

- **In-memory Storage**: Tasks are stored in a Python dictionary
- **CORS Enabled**: Allows frontend to communicate with backend
- **Pydantic Models**: Type validation for requests/responses
- **FastAPI**: Modern async Python web framework
