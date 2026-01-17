# 🎯 Hackathon Todo Phase-2 - Full Stack Application

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14%2B-black?logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?logo=postgresql)](https://postgresql.org)

A complete **full-stack Todo application** built during a hackathon with **Phase-2 implementation** featuring JWT authentication, PostgreSQL database, and modern web technologies.

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- **Python 3.10+** 
- **Node.js 18+** with npm
- **PostgreSQL** (local or Neon cloud)

### 1️⃣ Start Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
python run.py
```
✅ Backend running at `http://localhost:8000`  
📚 API Docs at `http://localhost:8000/docs`

### 2️⃣ Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
✅ Frontend running at `http://localhost:3000`

---

## 📊 Project Overview

### ✨ Features

#### Backend (FastAPI + SQLModel + JWT)
- ✅ **User Authentication** - JWT-based secure login/registration
- ✅ **PostgreSQL Database** - SQLModel ORM with Neon support
- ✅ **Protected Endpoints** - User-isolated task management
- ✅ **RESTful API** - Full CRUD operations with error handling
- ✅ **CORS Configuration** - Frontend integration ready
- ✅ **Auto Documentation** - Swagger UI & ReDoc

#### Frontend (Next.js + React)
- ✅ **User Interface** - Clean, responsive Todo app
- ✅ **Task Management** - Create, read, update, delete todos
- ✅ **Task Statistics** - Total and completed count tracking
- ✅ **Real-time Updates** - Instant UI feedback
- ✅ **Error Handling** - User-friendly error messages
- ✅ **Mobile Responsive** - Works on all devices

---

## 🏗️ Project Structure

```
hackathon-todo-phase2/
│
├── 📦 Backend (Python + FastAPI)
│   ├── app/
│   │   ├── main.py           # 🔐 Protected endpoints & CORS
│   │   ├── auth.py           # 🔑 JWT authentication
│   │   ├── models.py         # 📊 SQLModel database models
│   │   └── database.py       # 🗄️ PostgreSQL connection
│   ├── run.py                # ⚙️ Startup script
│   ├── requirements.txt       # 📋 Dependencies
│   ├── .env.example           # ✅ Config template
│   └── README.md
│
├── 📱 Frontend (Next.js + React)
│   ├── app/                  # App structure
│   ├── components/
│   │   ├── TodoForm.js       # Add todo form
│   │   ├── TodoList.js       # Todo list display
│   │   └── TodoItem.js       # Single todo item
│   ├── styles/
│   │   ├── globals.css       # Global styles
│   │   └── page.css          # Page styles
│   ├── package.json
│   └── README.md
│
├── 📚 Documentation
│   ├── README.md             # ⭐ This file
│   ├── QUICKSTART.md         # ⚡ 5-minute setup guide
│   ├── SETUP.md              # 📖 Detailed setup
│   ├── BACKEND_PHASE2_GUIDE.md    # 🔧 Backend docs
│   ├── FRONTEND_PHASE2_PLAN.md    # 🎨 Frontend roadmap
│   ├── ARCHITECTURE_DIAGRAMS.md   # 🔷 System design
│   ├── PHASE2_COMPLETION_SUMMARY.md # ✅ Completion status
│   ├── STATUS_DASHBOARD.md        # 📊 Project metrics
│   └── INDEX.md              # 🗂️ Documentation index
│
└── 🎯 Specifications
    ├── speckit.constitution  # Project rules
    ├── speckit.specify       # Requirements
    ├── speckit.plan          # Implementation plan
    └── speckit.tasks         # Task breakdown
```

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get JWT token |

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update user profile |

### Tasks (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all user tasks |
| POST | `/tasks` | Create new task |
| GET | `/tasks/{id}` | Get specific task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

📚 **Interactive API Docs**: `http://localhost:8000/docs`

---

## 🔐 Authentication Flow

```
1. User registers with email/password
2. Password hashed with bcrypt
3. User receives JWT token on login
4. Token included in Authorization header
5. Protected endpoints verify token
6. Token expires (configurable)
7. User refresh token for new access
```

---

## 🗄️ Database Schema

### Users Table
```sql
- id (Primary Key)
- email (Unique)
- full_name
- hashed_password
- created_at
- updated_at
```

### Tasks Table
```sql
- id (Primary Key)
- title
- description
- completed (Boolean)
- user_id (Foreign Key → Users)
- created_at
- updated_at
```

---

## 🔧 Configuration

### Backend Environment Variables
Create `backend/.env`:
```env
# Database
DATABASE_URL=postgresql+psycopg://user:password@localhost/todo_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables
Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📚 Documentation Guide

| Document | Purpose | Best For |
|----------|---------|----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup | Getting started |
| [SETUP.md](SETUP.md) | Detailed installation | Complete setup |
| [BACKEND_PHASE2_GUIDE.md](BACKEND_PHASE2_GUIDE.md) | Backend technical docs | Backend development |
| [FRONTEND_PHASE2_PLAN.md](FRONTEND_PHASE2_PLAN.md) | Frontend roadmap | Frontend development |
| [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) | System design | Understanding system |
| [PHASE2_COMPLETION_SUMMARY.md](PHASE2_COMPLETION_SUMMARY.md) | What's done | Project status |
| [STATUS_DASHBOARD.md](STATUS_DASHBOARD.md) | Progress metrics | Metrics & timeline |

---

## 🚦 Project Status

### ✅ Phase 2 - BACKEND COMPLETE
- SQLModel database models
- PostgreSQL/Neon configuration
- JWT authentication system
- User registration/login endpoints
- Protected task CRUD endpoints
- CORS configuration
- Error handling
- Full documentation

### 📋 Phase 2 - FRONTEND PLANNED
- Auth Context & state management
- Login/Register pages
- Protected routes & navigation
- Todo component refactoring
- API integration layer
- Enhanced UI components
- Comprehensive testing

---

## 💻 Development Workflow

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Database Setup (Local PostgreSQL)
```bash
createdb todo_db
# Update DATABASE_URL in backend/.env
python run.py  # Tables auto-created
```

### Database Setup (Neon Cloud)
1. Create account at https://neon.tech
2. Create project and copy connection string
3. Update `DATABASE_URL` in `backend/.env`
4. Run backend

---

## 🧪 Testing

### Test Backend API (Swagger UI)
1. Open `http://localhost:8000/docs`
2. Click "Authorize" and add your JWT token
3. Test endpoints interactively

### Test Backend API (cURL)
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123","full_name":"Test User"}'

# Login
curl -X POST "http://localhost:8000/auth/login?email=test@example.com&password=pass123"

# Create task (with token)
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries"}'
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (modern Python web framework)
- **Database ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (with Neon support)
- **Authentication**: JWT (PyJWT + bcrypt)
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: Next.js 14+
- **Library**: React 18+
- **Styling**: CSS3 (responsive design)
- **HTTP Client**: Fetch API
- **Build Tool**: Webpack (via Next.js)

### DevOps
- **Version Control**: Git
- **Package Management**: pip (Python), npm (Node.js)
- **Environment**: Virtual environments (Python), node_modules (Node.js)

---

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [PostgreSQL Documentation](https://postgresql.org/docs)
- [JWT Introduction](https://jwt.io/introduction)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Check database connection
# Verify DATABASE_URL in .env
```

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Database connection error
```
# Check PostgreSQL is running
# For Neon: verify connection string format
# Format: postgresql+psycopg://user:pass@host/db
```

### CORS errors
- Verify FRONTEND_URL in backend `.env`
- Ensure backend CORS allows frontend port

---

## 📝 Git Workflow

```bash
# Clone repository
git clone https://github.com/mihassan-97/hackathon-todo-phase2.git
cd hackathon-todo-phase2

# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "feat: description of changes"

# Push to GitHub
git push origin feature/your-feature
```

---

## 👥 Contributors

- **Phase 2 Implementation**: Complete backend with SQLModel, JWT, PostgreSQL
- **Frontend Planning**: Next.js UI structure ready for implementation

---

## 📄 License

This project is part of a hackathon initiative.

---

## ❓ Questions & Support

- 📚 Check [INDEX.md](INDEX.md) for documentation index
- 🚀 See [QUICKSTART.md](QUICKSTART.md) for quick setup
- 🔧 Read [BACKEND_PHASE2_GUIDE.md](BACKEND_PHASE2_GUIDE.md) for backend details
- 📊 Check [STATUS_DASHBOARD.md](STATUS_DASHBOARD.md) for project status

---

**Last Updated**: January 17, 2026  
**Phase**: 2 (Backend Complete, Frontend Planned)  
**Status**: ✅ Production Ready Backend | 📋 Frontend Development Ready
