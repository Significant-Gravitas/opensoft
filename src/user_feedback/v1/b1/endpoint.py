from http.client import HTTPException


from fastapi import Depends, APIRouter
from sqlmodel import Session

from src import engine
from src.user_feedback.v1.abstract_class import FeedbackRead, FeedbackCreate, Feedback


from fastapi import Depends, APIRouter, HTTPException

router = APIRouter()


@router.post("/user_feedback/", response_model=FeedbackRead)
async def feedback(feedback_data: FeedbackCreate):
    with Session(engine) as session:
        # Create Feedback instance
        feedback_instance = Feedback(user_id=feedback_data.user_id, content=feedback_data.content)
        session.add(feedback_instance)
        session.commit()
        session.refresh(feedback_instance)

    return feedback_instance

