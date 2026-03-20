from fastapi import FastAPI, HTTPException, status
from typing import List, Optional, Annotated

from fastapi.params import Form
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# Test des form data : format generalement utilisé lorsque les donnees a envoyer contiennent des fichiers
@app.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}