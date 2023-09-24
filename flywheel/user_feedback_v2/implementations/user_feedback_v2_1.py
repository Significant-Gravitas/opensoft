from http.client import HTTPException


from fastapi import Depends, APIRouter
from sqlmodel import Session

from flywheel import engine
from flywheel.user_feedback_v2.abstract_class import FeedbackRead, FeedbackCreate, Feedback

feedback_router = APIRouter()

from fastapi import Depends, APIRouter, HTTPException

feedback_router = APIRouter()

@feedback_router.post("/feedback/", response_model=FeedbackRead)
async def feedback(feedback_data: FeedbackCreate):
    with Session(engine) as session:
        # Create Feedback instance
        feedback_instance = Feedback(user_id=feedback_data.user_id, content=feedback_data.content)
        session.add(feedback_instance)
        session.commit()
        session.refresh(feedback_instance)

    return feedback_instance

