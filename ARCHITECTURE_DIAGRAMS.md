# Phase-2 Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        │                                         │
   ┌────▼──────┐                           ┌─────▼──────┐
   │ Frontend   │                           │  Backend   │
   │ Next.js    │◄──────── REST APIs ──────►│  FastAPI   │
   │ React 18   │        (JSON)             │  Python    │
   │ Port:3000  │                           │  Port:8000 │
   └────┬───────┘                           └─────┬──────┘
        │                                         │
        │ Token Storage                          │
        │ (localStorage)                         │
        │                                         │
        │                                   ┌─────▼───────────┐
        │                                   │  PostgreSQL /   │
        │                                   │  Neon Database  │
        │                                   │                 │
        │                                   │ Tables:         │
        │                                   │ - users         │
        │                                   │ - tasks         │
        │                                   └─────────────────┘
        │
        └──────────────────────┬──────────────────────┘
                               │
                        JWT Authentication
                        Bearer Tokens
```

---

## Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                          USERS                              │
├──────────────┬──────────────────────────────────────────────┤
│ id (PK)      │ INTEGER PRIMARY KEY                          │
│ email        │ VARCHAR UNIQUE NOT NULL                      │
│ full_name    │ VARCHAR                                      │
│ password     │ VARCHAR (hashed with bcrypt)                │
│ is_active    │ BOOLEAN DEFAULT TRUE                         │
│ created_at   │ TIMESTAMP DEFAULT CURRENT_TIMESTAMP          │
└─────────────────────────────────────────────────────────────┘
         │
         │ 1:N Relationship
         │
┌─────────────────────────────────────────────────────────────┐
│                          TASKS                              │
├──────────────┬──────────────────────────────────────────────┤
│ id (PK)      │ INTEGER PRIMARY KEY                          │
│ user_id (FK) │ INTEGER FOREIGN KEY → users.id               │
│ title        │ VARCHAR NOT NULL                             │
│ description  │ VARCHAR                                      │
│ completed    │ BOOLEAN DEFAULT FALSE                        │
│ created_at   │ TIMESTAMP DEFAULT CURRENT_TIMESTAMP          │
│ updated_at   │ TIMESTAMP DEFAULT CURRENT_TIMESTAMP          │
└─────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow

```
┌──────────────┐
│   User App   │
└──────┬───────┘
       │
       │ 1. POST /auth/register
       │    email, password, full_name
       │
       ▼
┌─────────────────────────────────┐
│  Backend: AuthService           │
│  - Validate email not taken      │
│  - Hash password (bcrypt)        │
│  - Create User record            │
└─────────────────────────────────┘
       │
       │ Store in DB
       │
       ▼
┌─────────────────────────────────┐
│  Database: users table          │
│  - id, email, hashed_pwd,...    │
└─────────────────────────────────┘
       │
       │ Return User object
       │
       ▼
┌──────────────┐
│   Frontend   │
│ Show success │
└──────────────┘


                    LOGIN FLOW
                    
┌──────────────┐
│   User App   │
└──────┬───────┘
       │
       │ 2. POST /auth/login
       │    email, password
       │
       ▼
┌──────────────────────────────────┐
│  Backend: AuthService            │
│  - Find user by email            │
│  - Verify password (bcrypt)      │
│  - Create JWT token              │
│    { sub: user_id,               │
│      email, full_name,           │
│      exp: now + 30min }          │
└──────────────────────────────────┘
       │
       │ Return token
       │
       ▼
┌──────────────┐
│   Frontend   │
│ Store token  │
│ localStorage │
└──────────────┘


                    PROTECTED REQUEST FLOW
                    
┌──────────────┐
│   Frontend   │
└──────┬───────┘
       │
       │ 3. GET /tasks
       │    Authorization: Bearer <JWT_TOKEN>
       │
       ▼
┌──────────────────────────────────┐
│  Backend: get_current_user()     │
│  - Extract token from header     │
│  - Decode JWT (verify signature) │
│  - Check expiration              │
│  - Return user_id & info         │
└──────────────────────────────────┘
       │
       ├─ Valid? ────────┐
       │                 │
       ▼                 ▼
┌──────────────┐   ┌──────────────┐
│  Fetch tasks │   │  401 Error   │
│  WHERE       │   │  Redirect to │
│  user_id = ? │   │  login page  │
└──────────────┘   └──────────────┘
       │
       ▼
┌──────────────┐
│   Frontend   │
│ Display      │
│ user's tasks │
└──────────────┘
```

---

## API Endpoint Map

```
FastAPI Application (http://localhost:8000)
│
├── Health Check
│   └── GET /
│       └── { "message": "Backend running", "version": "2.0.0" }
│
├── Authentication (Public)
│   ├── POST /auth/register
│   │   └── { email, password, full_name } → { User }
│   └── POST /auth/login
│       └── { email, password } → { access_token, token_type }
│
├── Users (Protected)
│   ├── GET /users/me
│   │   └── (requires valid JWT) → { User }
│   └── PUT /users/me
│       └── (requires valid JWT) → { User }
│
├── Tasks (Protected)
│   ├── GET /tasks
│   │   └── (requires valid JWT) → [ Task ]
│   ├── POST /tasks
│   │   └── (requires valid JWT) + { title, description } → { Task }
│   ├── GET /tasks/{id}
│   │   └── (requires valid JWT) → { Task }
│   ├── PUT /tasks/{id}
│   │   └── (requires valid JWT) + { updates } → { Task }
│   └── DELETE /tasks/{id}
│       └── (requires valid JWT) → { "message": "..." }
│
├── Documentation (Public)
│   ├── GET /docs
│   │   └── Interactive Swagger UI
│   └── GET /redoc
│       └── ReDoc documentation
│
└── OpenAPI Schema (Public)
    └── GET /openapi.json
        └── Machine-readable schema
```

---

## Request/Response Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT REQUEST                           │
│  POST /auth/login?email=...&password=...                    │
│  Content-Type: application/json                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI REQUEST PROCESSING                     │
│  1. Parse request (query/body)                              │
│  2. Validate with Pydantic                                  │
│  3. Execute endpoint function                               │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌─────────────────┐      ┌─────────────────┐
│ Validation Pass │      │ Validation Fail │
│ Process request │      │ Return 422 error│
└────────┬────────┘      └─────────────────┘
         │
         ├─ Check auth? ──┐
         │                │
         ▼                ▼
┌──────────────────┐  ┌──────────────┐
│ Decode JWT token │  │ 401 Unauth   │
│ Get user_id      │  │ Return error │
└────────┬─────────┘  └──────────────┘
         │
         ├─ Token valid? ──┐
         │                 │
         ▼                 ▼
┌───────────────────┐  ┌──────────────┐
│ Execute endpoint  │  │ 401 Expired  │
│ Database query    │  │ Return error │
│ Build response    │  └──────────────┘
└────────┬──────────┘
         │
         ▼
┌──────────────────────────────────────┐
│      FASTAPI RESPONSE BUILDING       │
│  1. Serialize response (Pydantic)    │
│  2. Add headers (Content-Type, etc.) │
│  3. Encode to JSON                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│       HTTP RESPONSE (JSON)         │
│  Status: 200 OK                    │
│  Content-Type: application/json    │
│  Body: { access_token, ... }       │
└────────┬───────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│           CLIENT BROWSER            │
│  Parse response                     │
│  Store token in localStorage        │
│  Update UI state                    │
└─────────────────────────────────────┘
```

---

## Frontend Architecture (Phase-2)

```
┌──────────────────────────────────────────────────────────┐
│                   Next.js App (Port 3000)                │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │           Root Layout (RootLayout)                │ │
│  │  - AuthContext Provider                           │ │
│  │  - Global styles                                  │ │
│  │                                                   │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │      Routing (App Router)                 │  │ │
│  │  │                                            │  │ │
│  │  │  / (home)                                  │  │ │
│  │  │  ├─ Redirect to login or dashboard        │  │ │
│  │  │  │                                         │  │ │
│  │  │  ├─ (auth)/ ─ Public routes               │  │ │
│  │  │  │  ├─ /login                             │  │ │
│  │  │  │  │  └─ LoginForm, validation, API call│  │ │
│  │  │  │  └─ /register                          │  │ │
│  │  │  │     └─ RegisterForm, validation, API  │  │ │
│  │  │  │                                         │  │ │
│  │  │  └─ (dashboard)/ ─ Protected routes       │  │ │
│  │  │     ├─ /                                  │  │ │
│  │  │     │  ├─ AuthGuard wrapper               │  │ │
│  │  │     │  ├─ DashboardLayout (Header+Nav)   │  │ │
│  │  │     │  ├─ TodoList component              │  │ │
│  │  │     │  └─ TodoForm component              │  │ │
│  │  │     │                                      │  │ │
│  │  │     ├─ /profile                           │  │ │
│  │  │     │  └─ User info, edit profile        │  │ │
│  │  │     │                                      │  │ │
│  │  │     └─ /settings                          │  │ │
│  │  │        └─ Account settings                │  │ │
│  │  │                                            │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  │                                                   │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │       Component Hierarchy                 │  │ │
│  │  │                                            │  │ │
│  │  │  Header                                    │  │ │
│  │  │  ├─ Logo                                   │  │ │
│  │  │  ├─ Nav Links                              │  │ │
│  │  │  └─ User Menu (Profile, Logout)           │  │ │
│  │  │                                            │  │ │
│  │  │  Sidebar (Optional)                        │  │ │
│  │  │  ├─ Dashboard link                         │  │ │
│  │  │  ├─ Settings link                          │  │ │
│  │  │  └─ Logout button                          │  │ │
│  │  │                                            │  │ │
│  │  │  TodoList                                  │  │ │
│  │  │  ├─ TodoItem (Reusable)                    │  │ │
│  │  │  │  ├─ Checkbox (completed toggle)        │  │ │
│  │  │  │  ├─ Title                               │  │ │
│  │  │  │  ├─ Edit button                         │  │ │
│  │  │  │  └─ Delete button (with confirmation)  │  │ │
│  │  │  └─ Empty state message                    │  │ │
│  │  │                                            │  │ │
│  │  │  TodoForm                                  │  │ │
│  │  │  ├─ Input: title (required)                │  │ │
│  │  │  ├─ Textarea: description (optional)       │  │ │
│  │  │  ├─ Submit button (create)                 │  │ │
│  │  │  └─ Loading spinner (on submit)            │  │ │
│  │  │                                            │  │ │
│  │  │  ErrorBoundary                             │  │ │
│  │  │  └─ Catch and display errors               │  │ │
│  │  │                                            │  │ │
│  │  │  Toast/Notification                        │  │ │
│  │  │  ├─ Success: task created                  │  │ │
│  │  │  ├─ Error: request failed                  │  │ │
│  │  │  └─ Info: action completed                 │  │ │
│  │  │                                            │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  │                                                   │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │      Context & State Management           │  │ │
│  │  │                                            │  │ │
│  │  │  AuthContext                               │  │ │
│  │  │  ├─ user (id, email, full_name)           │  │ │
│  │  │  ├─ token (JWT)                            │  │ │
│  │  │  ├─ isLoading                              │  │ │
│  │  │  ├─ isAuthenticated                        │  │ │
│  │  │  ├─ login(email, password)                 │  │ │
│  │  │  ├─ register(...)                          │  │ │
│  │  │  └─ logout()                               │  │ │
│  │  │                                            │  │ │
│  │  │  TodoContext                               │  │ │
│  │  │  ├─ todos: []                              │  │ │
│  │  │  ├─ isLoading                              │  │ │
│  │  │  ├─ getTodos()                             │  │ │
│  │  │  ├─ createTodo(title, desc)                │  │ │
│  │  │  ├─ updateTodo(id, updates)                │  │ │
│  │  │  └─ deleteTodo(id)                         │  │ │
│  │  │                                            │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  │                                                   │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │        API Services & Hooks               │  │ │
│  │  │                                            │  │ │
│  │  │  api.js (HTTP Client)                      │  │ │
│  │  │  ├─ baseURL: localhost:8000                │  │ │
│  │  │  ├─ Request interceptor (add token)        │  │ │
│  │  │  └─ Response interceptor (handle 401)      │  │ │
│  │  │                                            │  │ │
│  │  │  authService.js                            │  │ │
│  │  │  ├─ register(email, password, name)        │  │ │
│  │  │  ├─ login(email, password)                 │  │ │
│  │  │  ├─ logout()                               │  │ │
│  │  │  └─ getCurrentUser()                       │  │ │
│  │  │                                            │  │ │
│  │  │  todoService.js                            │  │ │
│  │  │  ├─ getTodos()                             │  │ │
│  │  │  ├─ getTodo(id)                            │  │ │
│  │  │  ├─ createTodo(data)                       │  │ │
│  │  │  ├─ updateTodo(id, data)                   │  │ │
│  │  │  └─ deleteTodo(id)                         │  │ │
│  │  │                                            │  │ │
│  │  │  Hooks                                      │  │ │
│  │  │  ├─ useAuth()                              │  │ │
│  │  │  ├─ useApi(url, options)                   │  │ │
│  │  │  └─ useTodo()                              │  │ │
│  │  │                                            │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  │                                                   │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
         │                  │
         │ XHR/Fetch        │ localStorage
         │                  │
         ▼                  ▼
    Backend API         JWT Token
    (8000)              + User Data
```

---

## Data Flow: Create Todo

```
User Input
    │
    ├─ Type: "Buy milk"
    │
    ▼
TodoForm Component
    │
    ├─ onChange → Update local state
    │
    ├─ Validate input (not empty)
    │
    ├─ onSubmit → Call handler
    │
    ▼
useTodo Hook
    │
    ├─ createTodo({ title, ... })
    │
    ├─ Call: todoService.createTodo(data)
    │
    ▼
todoService.js
    │
    ├─ POST /tasks
    │
    ├─ Headers:
    │  Authorization: Bearer <JWT>
    │  Content-Type: application/json
    │
    ├─ Body: { title, description, completed }
    │
    ▼
Backend (FastAPI)
    │
    ├─ Validate JWT token
    │
    ├─ Verify user authenticated
    │
    ├─ Insert into tasks table
    │  INSERT INTO task (user_id, title, ...)
    │  VALUES (?, ?, ...)
    │
    ├─ Return Task object
    │
    ▼
Frontend Response Handler
    │
    ├─ Update TodoContext state
    │  Add new task to todos array
    │
    ├─ Dispatch action (todoContext)
    │
    ├─ Trigger UI update
    │
    ├─ Show success toast
    │  "Todo created successfully!"
    │
    ├─ Clear form inputs
    │
    ▼
UI Render
    │
    ├─ TodoList re-renders
    │
    ├─ New TodoItem appears in list
    │
    ├─ Toast notification shown
    │
    ▼
User Sees: "Buy milk" in todo list ✓
```

---

## File Dependencies Map

```
main.py
├── depends on: models.py (Task, User, schemas)
├── depends on: auth.py (get_current_user, create_access_token)
├── depends on: database.py (get_session, engine)
└── imports: FastAPI, HTTPException, Session

models.py
├── depends on: SQLModel, Field, datetime
└── no other internal dependencies

auth.py
├── depends on: models.py (User, UserRead)
├── depends on: jose, passlib, FastAPI security
└── imports: JWT utilities, password hashing

database.py
├── depends on: models.py (SQLModel)
├── depends on: sqlalchemy
└── imports: Engine, Session, create_engine

requirements.txt
├── fastapi (web framework)
├── uvicorn (ASGI server)
├── sqlmodel (ORM + validation)
├── psycopg (PostgreSQL driver)
├── python-jose (JWT)
├── passlib (password hashing)
└── python-dotenv (env vars)
```

---

## Security Data Flow

```
Password Security
    │
    ├─ User enters: "MyPassword123"
    │
    ├─ Frontend sends HTTPS only (prod)
    │
    ├─ Backend receives: POST /auth/register
    │
    ├─ Hash password:
    │  bcrypt("MyPassword123") → "$2b$12$..."
    │
    ├─ Store hash in DB (never store plaintext!)
    │
    └─ ✓ Secure


JWT Token Security
    │
    ├─ Backend creates:
    │  { sub: 1, email: "user@mail.com", exp: 1234567890 }
    │
    ├─ Sign with SECRET_KEY:
    │  HMAC-SHA256(payload, SECRET_KEY)
    │
    ├─ Return to frontend:
    │  "eyJhbGc..." (JWT token)
    │
    ├─ Frontend stores in localStorage
    │
    ├─ Frontend adds to requests:
    │  Authorization: Bearer eyJhbGc...
    │
    ├─ Backend verifies:
    │  Decode and check signature
    │  Verify token not expired
    │
    └─ ✓ Secure


User Data Isolation
    │
    ├─ User A logs in → user_id = 1
    │
    ├─ Token contains: { sub: 1 }
    │
    ├─ User A requests: GET /tasks
    │
    ├─ Backend extracts user_id = 1
    │
    ├─ Database query:
    │  SELECT * FROM task WHERE user_id = 1
    │
    ├─ User A gets only their tasks ✓
    │
    └─ User B cannot see User A's tasks ✓
```

---

## Error Handling Flow

```
Request Received
    │
    ├─ 1. JSON Parse Error
    │  Response: 422 Unprocessable Entity
    │  Message: "Invalid JSON"
    │
    ├─ 2. Missing Required Field
    │  Response: 422 Unprocessable Entity
    │  Message: "field required"
    │
    ├─ 3. Invalid Data Type
    │  Response: 422 Unprocessable Entity
    │  Message: "value is not a valid integer"
    │
    ├─ 4. Missing Authorization Header
    │  Response: 403 Forbidden
    │  Message: "Not authenticated"
    │
    ├─ 5. Invalid JWT Token
    │  Response: 401 Unauthorized
    │  Message: "Invalid authentication credentials"
    │
    ├─ 6. Expired Token
    │  Response: 401 Unauthorized
    │  Message: "Token expired"
    │
    ├─ 7. Resource Not Found
    │  Response: 404 Not Found
    │  Message: "Task not found"
    │
    ├─ 8. Permission Denied
    │  Response: 403 Forbidden
    │  Message: "Not authorized to access this resource"
    │
    ├─ 9. Duplicate Email
    │  Response: 400 Bad Request
    │  Message: "Email already registered"
    │
    └─ 10. Server Error
       Response: 500 Internal Server Error
       Message: "Internal server error"


Frontend Response Handler
    │
    ├─ 2xx Success
    │  └─ Update state, show success toast
    │
    ├─ 4xx Client Error
    │  └─ Display error message to user
    │
    └─ 5xx Server Error
       └─ Show generic error, log to console
```

---

## Deployment Architecture (Future)

```
Internet Users
    │
    ├─ https://app.example.com (Frontend - Vercel)
    │  └─ Next.js deployed on Vercel
    │
    └─ https://api.example.com (Backend - Cloud Run/Railway)
       └─ FastAPI deployed on Cloud Run or Railway
            │
            └─ PostgreSQL (Neon)
               └─ Cloud database
```
