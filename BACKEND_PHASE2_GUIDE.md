# Backend Phase-II Implementation Guide

## Overview
The backend has been converted from Phase-I (in-memory tasks) to Phase-II with:
- ✅ SQLModel + PostgreSQL/Neon database integration
- ✅ JWT authentication system
- ✅ User and Task models with relationships
- ✅ Protected API endpoints

---

## Architecture

### Technology Stack
- **Framework**: FastAPI (modern Python web framework)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL / Neon (managed PostgreSQL)
- **Authentication**: JWT (python-jose + passlib)
- **Password Hashing**: bcrypt
- **CORS**: Enabled for localhost:3000 and localhost:3001

### Database Schema

#### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Tasks Table
```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER FOREIGN KEY REFERENCES user(id),
    title VARCHAR NOT NULL,
    description VARCHAR,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and endpoints
│   ├── models.py            # SQLModel definitions (User, Task, schemas)
│   ├── database.py          # Database connection and session
│   ├── auth.py              # JWT and password utilities
│   └── storage.py           # Deprecated (remove in cleanup)
├── .env                     # Local environment variables
├── .env.example             # Example environment file
├── requirements.txt         # Python dependencies
├── run.py                   # Server startup script
└── README.md                # Documentation
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Database

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL locally
# Create database
createdb todo_db

# Update .env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/todo_db
```

#### Option B: Neon (Recommended for production)
1. Sign up at https://neon.tech
2. Create a project and get connection string
3. Update `.env`:
```
DATABASE_URL=postgresql+psycopg://user:password@ep-xxx.region.neon.tech/todo_db
```

### 3. Configure JWT Secret
Update `.env`:
```
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### 4. Start Backend
```bash
python run.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## API Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-17T10:00:00"
}
```

#### Login User
```http
POST /auth/login?email=user@example.com&password=securepassword123

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /users/me
Authorization: Bearer <access_token>

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-17T10:00:00"
}
```

### Tasks

#### Get All Tasks (for current user)
```http
GET /tasks
Authorization: Bearer <access_token>

Response: 200 OK
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2024-01-17T10:00:00",
    "updated_at": "2024-01-17T10:00:00"
  }
]
```

#### Create Task
```http
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}

Response: 201 Created
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-01-17T10:00:00",
  "updated_at": "2024-01-17T10:00:00"
}
```

#### Update Task
```http
PUT /tasks/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Buy groceries and cook",
  "completed": true
}

Response: 200 OK
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries and cook",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2024-01-17T10:00:00",
  "updated_at": "2024-01-17T10:05:00"
}
```

#### Delete Task
```http
DELETE /tasks/1
Authorization: Bearer <access_token>

Response: 200 OK
{
  "message": "Task deleted successfully"
}
```

---

## Key Implementation Details

### 1. SQLModel Integration
- Models serve dual purpose: database schema + validation schema
- Table models inherit from both `SQLModel` and define `table=True`
- Schema models for API requests/responses (Create, Update, Read)
- Automatic ORM mapping

### 2. JWT Authentication
- Token structure: `{"sub": user_id, "email": user_email, "full_name": user_name}`
- Token expiry: 30 minutes (configurable)
- Refresh mechanism: Regenerate token on login
- Bearer token in Authorization header

### 3. Database Session Management
- Sessions handled via FastAPI dependency injection
- Session per request pattern
- Auto-close after response

### 4. CORS Configuration
- Allows localhost:3000 and localhost:3001
- Credentials enabled for same-origin requests
- Supports all HTTP methods and headers

### 5. Error Handling
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid credentials)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 500: Server Error

---

## Development Workflow

### Auto-reload
Edit any file and the server auto-restarts (configured in `run.py`):
```bash
python run.py --reload
```

### Database Migrations
SQLModel creates tables automatically on startup. For production:
- Use Alembic for migrations
- Track schema changes in version control
- Test migrations locally first

### Testing Endpoints
Use Swagger UI at `http://localhost:8000/docs`:
- Interactive API documentation
- Try endpoints directly
- View request/response schemas

---

## Environment Variables

Create `.env` file:
```
# Database
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/todo_db

# JWT
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

---

## Dependencies Breakdown

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `sqlmodel` | ORM + validation |
| `psycopg` | PostgreSQL driver |
| `python-jose` | JWT creation/verification |
| `passlib` | Password hashing |
| `python-dotenv` | Environment variables |
| `pydantic-settings` | Settings management |

---

## Security Considerations

### Implemented
✅ Password hashing with bcrypt
✅ JWT token expiration
✅ User isolation (users only see their own tasks)
✅ CORS restricted to trusted origins
✅ Input validation via Pydantic
✅ Unique email constraint

### TODO for Production
- [ ] Use HttpOnly, Secure cookies instead of localStorage
- [ ] Implement refresh token rotation
- [ ] Add rate limiting
- [ ] Add request logging
- [ ] Use HTTPS
- [ ] Add input sanitization
- [ ] Implement request signing
- [ ] Add brute-force protection

---

## Common Issues & Solutions

### Issue: "No module named 'sqlmodel'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "Cannot connect to database"
**Solution**: Check DATABASE_URL and PostgreSQL is running

### Issue: "JWT decode error"
**Solution**: Ensure SECRET_KEY matches between login and request

### Issue: "CORS error from frontend"
**Solution**: Frontend running on different port - add to CORS origins

---

## Next Steps for Frontend Integration

1. Frontend at `http://localhost:3000`
2. Register new user via `/auth/register`
3. Login and get JWT token via `/auth/login`
4. Include token in all subsequent requests:
   ```
   Authorization: Bearer <token>
   ```
5. Implement protected routes in frontend

---

## Useful Commands

```bash
# Create database
createdb todo_db

# Drop database
dropdb todo_db

# Check database connection
psql postgres -U postgres

# View database tables
\dt

# View specific table
\d task

# Run with auto-reload
python run.py --reload

# Check installed packages
pip list

# Generate requirements
pip freeze > requirements.txt
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [JWT.io](https://jwt.io/)
- [Neon Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
