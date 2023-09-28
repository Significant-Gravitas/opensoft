from fastapi import APIRouter
from sqlmodel import Session

from src import engine
from src.user_feedback.v1.models import Feedback, FeedbackCreate, FeedbackRead

router = APIRouter()


@router.post("/user_feedback/", response_model=FeedbackRead)
async def feedback(feedback_data: FeedbackCreate):
    feedback = Feedback(**feedback_data.dict())
    with Session(engine) as session:
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
    return feedback
