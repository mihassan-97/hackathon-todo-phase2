# 🚀 Todo App - Phase 2 Complete Setup Guide

## ✅ Project Status

**Phase-2 COMPLETE** - Spec-Driven Development with Full Stack Implementation

- ✅ Specifications (Constitution, Specify, Plan, Tasks)
- ✅ Backend: FastAPI with complete CRUD APIs
- ✅ Frontend: Next.js with full UI
- ✅ Integration: Frontend ↔ Backend via REST APIs

---

## 📋 Prerequisites

### System Requirements
- **Python 3.10+** (preferably Python 3.11 or 3.14)
- **Node.js 18+** with npm 9+
- **Git** for version control

### Verify Installation
```bash
python --version      # Should be 3.10+
node --version        # Should be 18+
npm --version         # Should be 9+
git --version         # Should be 2.30+
```

---

## 🏗️ Project Structure

```
hackathon-todo-phase2/
├── backend/                    # FastAPI Backend
│   ├── main.py               # Core API endpoints
│   ├── models.py             # Pydantic data models
│   ├── run.py                # Startup script
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
│
├── frontend/                   # Next.js Frontend
│   ├── app/
│   │   ├── page.js          # Main application page
│   │   └── layout.js        # Root layout
│   ├── styles/
│   │   ├── globals.css      # Global styles
│   │   └── page.css         # Page styles
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── README.md            # Frontend documentation
│
├── speckit.constitution       # Project rules
├── speckit.specify           # Requirements
├── speckit.plan              # Implementation plan
├── speckit.tasks             # Task breakdown
└── README.md                 # This file
```

---

## 🚀 Quick Start (2 Terminals)

### Terminal 1: Start Backend
```bash
cd backend
pip install -r requirements.txt
python run.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Expected output:
```
▲ Next.js 14.2.35
- Local:        http://localhost:3000
```

---

## 🌐 Access the Application

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://localhost:3000 | Main Todo App UI |
| **API** | http://localhost:8000 | FastAPI server |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **API ReDoc** | http://localhost:8000/redoc | ReDoc documentation |

---

## 📚 API Endpoints

### Health Check
```bash
curl http://localhost:8000/
```

### Get All Tasks
```bash
curl http://localhost:8000/tasks
```

### Create Task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries"}'
```

### Update Task
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries and cook","completed":true}'
```

### Delete Task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

## 🛠️ Development Workflow

### Backend Development
- Auto-reload enabled with `--reload` flag in `run.py`
- Edit `main.py` or `models.py` → Server auto-restarts
- View changes at http://localhost:8000/docs

### Frontend Development
- Hot-reload enabled by default in Next.js
- Edit files in `app/` or `styles/` → Changes appear instantly
- View changes at http://localhost:3000

### Making Changes

**Backend API change:**
1. Edit `main.py` endpoints or `models.py` schemas
2. Server auto-reloads
3. Test at http://localhost:8000/docs

**Frontend UI change:**
1. Edit `app/page.js` or CSS files
2. Browser auto-refreshes
3. Changes appear at http://localhost:3000

---

## ✨ Features Implemented

### Backend (FastAPI)
- ✅ POST `/tasks` - Create task
- ✅ GET `/tasks` - Get all tasks
- ✅ GET `/tasks/{id}` - Get specific task
- ✅ PUT `/tasks/{id}` - Update task
- ✅ DELETE `/tasks/{id}` - Delete task
- ✅ DELETE `/tasks` - Clear all tasks
- ✅ CORS enabled for frontend
- ✅ Automatic API documentation
- ✅ Input validation with Pydantic

### Frontend (Next.js)
- ✅ View all tasks with real-time updates
- ✅ Add new task with form
- ✅ Mark task as complete/incomplete
- ✅ Edit task title (double-click)
- ✅ Delete individual tasks
- ✅ Task statistics (total & completed count)
- ✅ Error handling with user messages
- ✅ Responsive mobile-friendly design
- ✅ Beautiful gradient UI with animations
- ✅ Loading states

---

## 🔧 Troubleshooting

### Backend won't start
**Issue:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt --only-binary :all:
python run.py
```

### Frontend npm install fails
**Issue:** Package conflicts or version issues

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run dev
```

### Port already in use
**Backend (port 8000):**
```bash
# Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend (port 3000):**
```bash
# Kill process using port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

Or change port in `run.py` (backend) or `npm run dev -- -p 3001` (frontend)

### CORS errors in browser console
- ✅ Already enabled in backend (`CORSMiddleware` in `main.py`)
- Verify both servers are running
- Check API URL in frontend environment variables

---

## 📝 Data Storage

**Note:** All data is stored in-memory during Phase-2

- Tasks are stored in a Python dictionary: `tasks_db`
- Data is cleared on server restart
- No database persistence
- Ready for Phase-3 database integration

---

## 🚢 Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
npm start
```

### Run Backend with Gunicorn (Production)
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:3000
- [ ] Can create a task in UI
- [ ] Task appears in API GET /tasks
- [ ] Can mark task complete
- [ ] Can delete task
- [ ] No console errors in browser

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review API docs at http://localhost:8000/docs
3. Check frontend console for errors (F12)
4. Check backend terminal for error messages

---

**Status:** ✅ Phase-2 Complete - Ready for Phase-3 Database Integration
