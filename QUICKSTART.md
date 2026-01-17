# ⚡ Quick Start Guide - Phase 2

## 🚀 Get Backend Running in 5 Minutes

### Prerequisites
- Python 3.10+ installed
- PostgreSQL installed locally OR Neon account

### Option A: Local PostgreSQL

```bash
# 1. Create database
createdb todo_db

# 2. Navigate to backend
cd backend

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
python run.py

# ✓ Backend running at http://localhost:8000
# ✓ API docs at http://localhost:8000/docs
```

### Option B: Neon (Cloud PostgreSQL)

```bash
# 1. Get connection string from https://neon.tech
# Should look like: postgresql+psycopg://user:pass@ep-xxx.region.neon.tech/dbname

# 2. Update backend/.env
DATABASE_URL=postgresql+psycopg://user:pass@ep-xxx.region.neon.tech/dbname

# 3. Navigate to backend
cd backend

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start server
python run.py

# ✓ Backend running at http://localhost:8000
```

---

## 🧪 Test Backend API

### Using Swagger UI (Recommended)
Open: http://localhost:8000/docs

### Using cURL

#### 1. Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

#### 2. Login & Get Token
```bash
curl -X POST "http://localhost:8000/auth/login?email=user@example.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Create Todo (Replace TOKEN with actual token)
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }'
```

#### 4. Get All Todos (Replace TOKEN)
```bash
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer TOKEN"
```

#### 5. Update Todo (Replace TOKEN and ID)
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true,
    "title": "Groceries done!"
  }'
```

#### 6. Delete Todo (Replace TOKEN and ID)
```bash
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer TOKEN"
```

---

## 🎨 Start Frontend (Once Backend Ready)

### Terminal 2: Frontend

```bash
cd frontend
npm install
npm run dev

# ✓ Frontend running at http://localhost:3000
```

---

## 📋 Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
python run.py --reload

# View database
psql todo_db

# List tables
\dt

# Drop and recreate database
dropdb todo_db && createdb todo_db

# Check Python version
python --version

# Install single package
pip install sqlmodel
```

### Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Start production build
npm start

# Clean node_modules
rm -rf node_modules && npm install
```

---

## 🆘 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error**: `psycopg.OperationalError: connection failed`
```bash
# Solution: Check PostgreSQL is running and DATABASE_URL is correct
# For local: createdb todo_db
# For Neon: Check connection string in .env
```

**Error**: `JWT decode error`
```bash
# Solution: Ensure SECRET_KEY in .env is configured
# The backend and frontend must use same SECRET_KEY
```

### Frontend won't start

**Error**: `Module not found: Next.js`
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Error**: `CORS error when calling API`
```bash
# Solution: Check backend is running on port 8000
# Check frontend is on localhost:3000
# Verify CORS middleware in main.py allows both ports
```

---

## 📚 Key Files

### Backend
- **[BACKEND_PHASE2_GUIDE.md](BACKEND_PHASE2_GUIDE.md)** - Full backend documentation
- [backend/app/main.py](backend/app/main.py) - API endpoints
- [backend/app/models.py](backend/app/models.py) - Database models
- [backend/app/auth.py](backend/app/auth.py) - JWT authentication
- [backend/app/database.py](backend/app/database.py) - Database connection

### Frontend
- **[FRONTEND_PHASE2_PLAN.md](FRONTEND_PHASE2_PLAN.md)** - Frontend roadmap
- [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) - Visual architecture
- [PHASE2_COMPLETION_SUMMARY.md](PHASE2_COMPLETION_SUMMARY.md) - What's completed

---

## 🔐 Security Notes

1. **Change SECRET_KEY** in `.env` before production
2. **Use HTTPS** in production
3. **Never commit .env** to git
4. **Use strong passwords** in database
5. **Add rate limiting** for production

---

## 🎯 Next Steps

1. ✅ Backend is ready
2. ⏳ Frontend implementation (see FRONTEND_PHASE2_PLAN.md)
3. 🔗 Connect frontend to backend
4. 📱 Test on mobile devices
5. 🚀 Deploy to production

---

## 📞 Reference

### API Documentation
- Live: http://localhost:8000/docs
- Raw: http://localhost:8000/openapi.json

### Ports
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Database: `localhost:5432`

### Default Credentials (Local Dev)
- Database: `postgres:postgres`
- Email: `user@example.com`
- Password: `securepassword123`

---

## ✅ Checklist

- [ ] PostgreSQL installed/Neon account created
- [ ] Backend dependencies installed
- [ ] `.env` file configured with DATABASE_URL
- [ ] Backend server running (http://localhost:8000)
- [ ] Tested registration and login endpoints
- [ ] Frontend dependencies installed
- [ ] Frontend server running (http://localhost:3000)
- [ ] Verified CORS working (no errors in console)
- [ ] Created test user and todo
- [ ] Documentation reviewed

---

**Ready to build Phase-2! 🚀**
