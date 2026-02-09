# import os
# from contextlib import asynccontextmanager
# from typing import List, Optional
# from fastapi import FastAPI, HTTPException
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from dotenv import load_dotenv
# from openai import OpenAI
# import os

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @app.post("/chat") # pyright: ignore[reportUndefinedVariable]
# async def chat_with_agent(message: str):
#     # Ye simple version hai jo user ki baat se task nikalta hai
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a Todo assistant. Extract tasks from user input."},
#             {"role": "user", "content": message}
#         ]
#     )
#     # Mazeed functionality (OpenAI Agents SDK) hum agle step mein tool calling ke sath add karenge
#     return {"reply": response.choices[0].message.content}

# load_dotenv()

# # Data Model
# class Todo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     description: Optional[str] = None
#     is_completed: bool = False

# # Database Engine
# engine = create_engine(os.getenv("DATABASE_URL"))

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield

# app = FastAPI(lifespan=lifespan)

# @app.post("/tasks", response_model=Todo)
# def create_task(todo: Todo):
#     with Session(engine) as session:
#         session.add(todo)
#         session.commit()
#         session.refresh(todo)
#         return todo

# @app.get("/tasks", response_model=List[Todo])
# def read_tasks():
#     with Session(engine) as session:
#         return session.exec(select(Todo)).all()

# @app.patch("/tasks/{todo_id}", response_model=Todo)
# def update_task(todo_id: int, todo_data: Todo):
#     with Session(engine) as session:
#         db_todo = session.get(Todo, todo_id)
#         if not db_todo:
#             raise HTTPException(status_code=404, detail="Not found")
#         data = todo_data.model_dump(exclude_unset=True)
#         db_todo.sqlmodel_update(data)
#         session.add(db_todo)
#         session.commit()
#         session.refresh(db_todo)
#         return db_todo
#     if __name__ == "__main__":
#      import uvicorn
#      uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)




import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import load_dotenv
from openai import OpenAI
import json

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware( # pyright: ignore[reportUndefinedVariable]
    CORSMiddleware,
    allow_origins=["*"], # Ya "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_completed: bool = False

engine = create_engine(os.getenv("DATABASE_URL"))

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Tools for AI
def add_todo(title: str):
    with Session(engine) as session:
        todo = Todo(title=title)
        session.add(todo)
        session.commit()
        return f"Added task: {title}"

def list_todos():
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return [t.title for t in todos]

@app.post("/chat")
async def chat(prompt: str):
    # AI ko tools ki definition dena
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_todo",
                "description": "Add a new task to the todo list",
                "parameters": {"type": "object", "properties": {"title": {"type": "string"}}}
            }
        },
        {
            "type": "function",
            "function": { "name": "list_todos", "description": 
                         "Get all tasks" }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        tools=tools
    )

    # Agar AI function call karna chahta hai
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name == "add_todo":
                args = json.loads(tool_call.function.arguments)
                result = add_todo(args['title'])
                return {"reply": result}
            elif tool_call.function.name == "list_todos":
                result = list_todos()
                return {"reply": f"Your tasks are: {', '.join(result)}"}
    
    return {"reply": response.choices[0].message.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)