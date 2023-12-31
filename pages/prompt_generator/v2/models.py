from pydantic import BaseModel
from sqlmodel import SQLModel


class PromptBase(SQLModel, BaseModel):
    module_backend: str
    goal: str


class PromptRead(PromptBase):
    prompt: str


class PromptCreate(PromptBase):
    pass
