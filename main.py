from fastapi import FastAPI, HTTPException
from models import Todo, todo_pydantic, todo_in_pydantic
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    message: str

class HTTPNotFoundError(BaseModel):
    detail: str

app = FastAPI()


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',  # a modifier pour utiliser postgresql
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/todos", response_model=List[todo_pydantic])
async def get_all_todo():
    return await todo_pydantic.from_queryset(Todo.all())


@app.get("/todos/{todo_id}", response_model=todo_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_todo(todo_id: int):
    try:
        return await todo_pydantic.from_queryset_single(Todo.get(id=todo_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", response_model=todo_pydantic)
async def create_todo(todo: todo_in_pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True)) # exclude_unset=True : ignore les champs non fournis (optionnels)
    return await todo_pydantic.from_tortoise_orm(todo_obj)


@app.put("/todos/{todo_id}", response_model=todo_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_todo(todo_id: int, new_todo: todo_in_pydantic):
    updated_count = await Todo.filter(id=todo_id).update(**new_todo.dict(exclude_unset=True))
    if not updated_count:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await todo_pydantic.from_queryset_single(Todo.get(id=todo_id))


@app.delete("/todos/{todo_id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_todo(todo_id: int):
    deleted_count = await Todo.filter(id=todo_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Message(message="delete successfully")