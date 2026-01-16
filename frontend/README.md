# Frontend - Todo App (Next.js)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Environment Variables

Create a `.env.local` file to configure the backend API URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features

- ✅ View all tasks
- ✅ Add new task with title
- ✅ Mark task as completed/incomplete
- ✅ Delete task
- ✅ Edit task title (double-click to edit)
- ✅ Task statistics (total and completed count)
- ✅ Responsive design (mobile-friendly)
- ✅ Real-time error handling
- ✅ Loading states

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── page.js           # Main page component with all functionality
│   └── layout.js         # Root layout
├── styles/
│   ├── globals.css       # Global styles
│   └── page.css          # Page-specific styles
├── package.json
├── next.config.js
├── tsconfig.json
└── README.md
```

## Technologies

- Next.js 14 - React framework
- Axios - HTTP client
- CSS - Styling

## API Integration

The frontend communicates with the FastAPI backend using REST APIs:

- `GET /tasks` - Fetch all tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

## Styling

- Modern gradient background (purple theme)
- Clean card-based UI
- Smooth transitions and hover effects
- Mobile responsive design
- Accessible color contrast
