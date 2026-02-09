# Backend API Spec
Build a FastAPI application with the following:
1. Endpoints:
   - GET /tasks (Fetch all)
   - POST /tasks (Create new)
   - PATCH /tasks/{id} (Update status/content)
   - DELETE /tasks/{id} (Remove task)
2. Integration: Connect with Neon DB using SQLModel.
3. Environment: Use .env file for DATABASE_URL.