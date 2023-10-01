from enum import Enum

from pydantic import BaseModel
from sqlmodel import SQLModel

class GoalEnum(str, Enum):
    pass_tests = "pass_tests"
    pass_frontend_tests = "pass_frontend_tests"
class PromptBase(SQLModel, BaseModel):
    module_backend: str
    goal: GoalEnum


class PromptRead(PromptBase):
    prompt: str


class PromptCreate(PromptBase):
    pass
