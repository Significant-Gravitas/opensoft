from abc import ABC, abstractmethod
from typing import Any

from fastapi import FastAPI
from sqlmodel import SQLModel, Field

from flywheel.base_class import BaseClass
app = FastAPI()


# Define a class for creating feedback
class FeedbackBase(SQLModel):
    user_id: int
    content: str

class FeedbackRead(FeedbackBase):
    id: int

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase, table=True):
    id: int = Field(default=None, primary_key=True)

class AbstractUserFeedbackV1(ABC, BaseClass):

    @classmethod
    @abstractmethod
    @app.post("/feedback", response_model=FeedbackRead)
    def create_feedback(cls, feedback: FeedbackCreate):
        pass
