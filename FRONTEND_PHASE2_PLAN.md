# Frontend Phase-II Plan: Auth + UI + API Binding

## Overview
Convert the frontend from Phase-I (basic Todo list) to Phase-II with:
- ✅ JWT Authentication (Login/Register)
- ✅ Protected routes and state management
- ✅ API integration with new backend endpoints
- ✅ Enhanced UI components
- ✅ Token storage and refresh logic

---

## Architecture

### Technology Stack
- **Framework**: Next.js 13.5+ (App Router)
- **UI**: React 18.2+ with CSS Modules
- **State Management**: React Context API + useReducer
- **HTTP Client**: Fetch API (built-in)
- **Auth Storage**: localStorage (JWT token)
- **Styling**: CSS Modules + Tailwind CSS (optional)

### Folder Structure
```
frontend/
├── app/
│   ├── layout.js              # Root layout with Auth context
│   ├── page.js                # Home/redirect to login or dashboard
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.js       # Login page
│   │   ├── register/
│   │   │   └── page.js       # Register page
│   │   └── layout.js         # Auth layout (no protection)
│   └── (dashboard)/
│       ├── layout.js         # Dashboard layout (protected)
│       ├── page.js           # Todo list page
│       ├── settings/
│       │   └── page.js       # User settings page
│       └── profile/
│           └── page.js       # User profile page
├── components/
│   ├── auth/
│   │   ├── LoginForm.js      # Login form
│   │   ├── RegisterForm.js   # Register form
│   │   └── AuthGuard.js      # Protected route wrapper
│   ├── todos/
│   │   ├── TodoList.js       # List of todos
│   │   ├── TodoItem.js       # Individual todo item
│   │   ├── TodoForm.js       # Create/edit form
│   │   └── TodoActions.js    # Delete, toggle complete
│   ├── layout/
│   │   ├── Header.js         # Top navigation
│   │   ├── Sidebar.js        # Side navigation
│   │   └── Footer.js         # Footer
│   └── common/
│       ├── LoadingSpinner.js # Loading indicator
│       ├── ErrorBoundary.js  # Error handler
│       └── Toast.js          # Notifications
├── context/
│   ├── AuthContext.js        # Auth state management
│   └── TodoContext.js        # Todo state management
├── hooks/
│   ├── useAuth.js            # Auth hook
│   ├── useApi.js             # API call wrapper
│   └── useTodo.js            # Todo operations hook
├── services/
│   ├── api.js                # API client setup
│   ├── authService.js        # Auth API calls
│   └── todoService.js        # Todo API calls
├── styles/
│   ├── globals.css           # Global styles
│   ├── Auth.module.css       # Auth pages styles
│   ├── Dashboard.module.css  # Dashboard styles
│   └── Todo.module.css       # Todo component styles
├── utils/
│   ├── constants.js          # App constants
│   ├── validators.js         # Form validators
│   └── helpers.js            # Helper functions
├── middleware.js             # NextAuth or custom middleware
├── package.json
├── next.config.js
└── tsconfig.json
```

---

## Implementation Steps

### Phase 2A: Authentication System (Priority: HIGH)

#### 1.1 Create Auth Context & Provider
- **File**: `app/context/AuthContext.js`
- **Features**:
  - Store user state (id, email, full_name, is_active)
  - Store auth token (JWT)
  - Auth status (isLoading, isAuthenticated, isError)
  - Methods: login, register, logout, refreshToken
  - Persist token in localStorage

#### 1.2 Implement Auth API Service
- **File**: `app/services/authService.js`
- **Endpoints**:
  - `POST /auth/register` - Create new account
  - `POST /auth/login` - Get JWT token
  - `GET /users/me` - Get current user info
  - `PUT /users/me` - Update profile
- **Features**:
  - Auto-attach JWT token to all requests
  - Handle 401 errors (redirect to login)
  - Refresh token logic (optional)

#### 1.3 Create Login Page
- **File**: `app/(auth)/login/page.js`
- **Features**:
  - Email + Password form
  - Validation
  - Error handling
  - Loading state
  - Redirect to dashboard on success
  - Link to register page

#### 1.4 Create Register Page
- **File**: `app/(auth)/register/page.js`
- **Features**:
  - Email + Password + Confirm Password + Full Name form
  - Password strength validator
  - Email validation
  - Duplicate email check
  - Redirect to login on success
  - Link to login page

#### 1.5 Create Protected Routes (AuthGuard)
- **File**: `app/components/auth/AuthGuard.js`
- **Features**:
  - Check if user authenticated
  - Redirect to login if not
  - Show loading spinner while checking
  - Handle token expiration

---

### Phase 2B: Todo Management (Priority: HIGH)

#### 2.1 Create Todo Context & Service
- **File**: `app/context/TodoContext.js`, `app/services/todoService.js`
- **Features**:
  - Store todos state
  - Methods: getTodos, createTodo, updateTodo, deleteTodo
  - Loading states per action
  - Error handling

#### 2.2 Refactor Todo Components
- **TodoList.js**: Fetch and display user's todos
- **TodoForm.js**: Create new todo with API call
- **TodoItem.js**: Display, edit, toggle complete
- **TodoActions.js**: Delete button with confirmation

#### 2.3 Create Dashboard Layout
- **File**: `app/(dashboard)/layout.js`
- **Features**:
  - Protected route wrapper
  - Header with user info
  - Sidebar navigation
  - Logout button
  - Active route highlighting

#### 2.4 Create Main Todo Page
- **File**: `app/(dashboard)/page.js`
- **Features**:
  - Display user's todos from API
  - Real-time list updates
  - Create new todo form
  - Filter/sort options (optional)
  - Empty state message

---

### Phase 2C: UI/UX Improvements (Priority: MEDIUM)

#### 3.1 Create Reusable Components
- **LoadingSpinner.js**: Show during async operations
- **ErrorBoundary.js**: Catch component errors
- **Toast.js**: Notifications (success, error, warning)
- **Header.js**: Navigation with user menu
- **Sidebar.js**: Left navigation menu

#### 3.2 Add Form Validation
- Email format validation
- Password strength (8+ chars, mixed case, numbers)
- Required fields
- Real-time error feedback
- Success/error messages

#### 3.3 Implement Loading States
- Loading spinner on buttons
- Disable form during submission
- Show loading indicator on page load
- Optimize UX with debouncing

#### 3.4 Add Error Handling
- Display user-friendly error messages
- Network error recovery
- Timeout handling
- Log errors to console (dev only)

---

### Phase 2D: API Integration (Priority: HIGH)

#### 4.1 Setup API Client
- **File**: `app/services/api.js`
- **Features**:
  - Base URL configuration (localhost:8000)
  - Default headers (Content-Type, Authorization)
  - Request interceptor (add JWT token)
  - Response interceptor (handle errors)
  - Timeout handling

#### 4.2 Create API Hooks
- **useApi.js**: Generic fetch wrapper with loading/error state
- **useAuth.js**: Auth-related operations
- **useTodo.js**: Todo CRUD operations

#### 4.3 Handle CORS
- Backend configured for localhost:3000
- Frontend requests include credentials
- Handle preflight requests

#### 4.4 Token Management
- Store JWT in localStorage on login
- Add token to Authorization header
- Clear token on logout
- Handle token expiration (401)

---

### Phase 2E: Settings & Profile (Priority: LOW)

#### 5.1 Create User Profile Page
- **File**: `app/(dashboard)/profile/page.js`
- **Features**:
  - Display user info
  - Edit full name
  - View account created date
  - View email

#### 5.2 Create Settings Page
- **File**: `app/(dashboard)/settings/page.js`
- **Features**:
  - Change password (if implemented in backend)
  - Theme toggle (optional)
  - Notification preferences (optional)
  - Delete account (optional)

---

## Development Timeline

### Week 1: Authentication
- Day 1-2: Auth Context + API Service
- Day 3-4: Login & Register pages
- Day 5: Protected routes + testing

### Week 2: Todo Management
- Day 1-2: Todo Context + refactor components
- Day 3-4: Dashboard layout + main page
- Day 5: Testing + bug fixes

### Week 3: Polish & Deploy
- Day 1-2: UI improvements + error handling
- Day 3-4: Performance optimization
- Day 5: Deploy to production

---

## Dependencies to Install

```bash
npm install --save-dev tailwindcss postcss autoprefixer  # Optional for styling
```

OR use plain CSS (already in project structure)

---

## API Integration Checklist

- [ ] Auth Context setup and token storage
- [ ] Login/Register forms with validation
- [ ] Protected route wrapper (AuthGuard)
- [ ] Auto-attach JWT token to requests
- [ ] Handle 401 errors (logout & redirect)
- [ ] Todo CRUD operations with API
- [ ] Loading spinners + error messages
- [ ] localStorage cleanup on logout
- [ ] Dashboard layout with user menu
- [ ] Profile and settings pages

---

## Key Features Phase-2

### Authentication
✅ User registration with email validation
✅ User login with JWT token
✅ Protected routes
✅ Token persistence
✅ Auto-logout on token expiry
✅ User profile display

### Todo Management
✅ Create todo (requires auth)
✅ Read todos (user-specific)
✅ Update todo (title, description, completed)
✅ Delete todo (with confirmation)
✅ Real-time list updates

### UI/UX
✅ Responsive design
✅ Loading indicators
✅ Error messages
✅ Form validation
✅ Toast notifications
✅ Empty states

---

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Testing Checklist

- [ ] Register new user
- [ ] Login with registered email
- [ ] Create todo (verify in DB)
- [ ] Update todo completion status
- [ ] Delete todo (with confirmation)
- [ ] Logout and verify redirect to login
- [ ] Try accessing dashboard without token
- [ ] Check error messages for invalid inputs
- [ ] Test with slow network (DevTools)
- [ ] Test on mobile (responsive design)

---

## Performance Considerations

- Lazy load route components
- Memoize Context consumers
- Debounce search/filter operations
- Cache API responses (optional)
- Use dynamic imports for heavy libraries

---

## Security Considerations

- Store JWT in localStorage (acceptable for SPAs)
- Add HttpOnly cookie support (future enhancement)
- CSRF token (if using forms)
- XSS prevention (sanitize user input)
- Rate limiting (backend-side)
- Secure headers (backend-side)

---

## Future Enhancements (Phase-3)

- [ ] Real-time updates with WebSockets
- [ ] Todo categories/tags
- [ ] Due dates and reminders
- [ ] Sharing todos with others
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Mobile app with React Native
- [ ] Analytics dashboard
