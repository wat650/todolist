from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Todo(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    date = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)

    class PydanticMeta:
        pass

todo_pydantic = pydantic_model_creator(Todo, name="Todo")
todo_in_pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)