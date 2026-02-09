# Frontend Spec (Next.js)
1. Framework: Next.js with TypeScript and Tailwind CSS.
2. Components:
   - `TaskForm`: Input field and 'Add' button.
   - `TaskList`: Display tasks with checkboxes and delete buttons.
   - `TaskItem`: Individual row showing title and status.
3. State Management: Use React `useState` and `useEffect` to fetch data from FastAPI.
4. API Integration: Call http://localhost:8000/tasks for all CRUD operations.