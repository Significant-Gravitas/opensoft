from pydantic import constr
from sqlmodel import Field, SQLModel


# Define a class for creating feedback
class FeedbackBase(SQLModel):
    user_id: int
    content: constr(min_length=1)


class FeedbackRead(FeedbackBase):
    id: int


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase, table=True):
    id: int = Field(default=None, primary_key=True)


# the following acts as an contract for the routes

# @app.post("/feedback/", response_model=FeedbackRead)
# def create_feedback(feedback: FeedbackCreate):
#     pass
