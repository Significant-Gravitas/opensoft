from fastapi import APIRouter
from sqlmodel import Session

from pages import engine
from pages.user_feedback.v1.models import Feedback, FeedbackCreate, FeedbackRead

router = APIRouter()


@router.post("/user_feedback/", response_model=FeedbackRead)
async def feedback(feedback_data: FeedbackCreate):
  pass
