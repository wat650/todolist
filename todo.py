from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel


app = FastAPI(title="ToDo API", version="1.0")

class Todo(BaseModel):
    name: str
    date: str
    description: Optional[str] = None
    completed: bool = False

store_todo: List[Todo] = []

@app.get('/')
async def root():
    return {"message": "Welcome to my ToDo List"}


@app.get("/todos", response_model=List[Todo])
async def get_all_todos():
    return store_todo


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    try:
        return store_todo[todo_id]
    except:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos")
async def create_todo(todo: Todo):
    store_todo.append(todo)
    return todo


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, new_todo: Todo):
    try:
        store_todo[todo_id] = new_todo
        return new_todo
    except:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    try:
        obj = store_todo[todo_id]
        store_todo.pop(todo_id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="todo not found")
