from fastapi import APIRouter
from sqlmodel import Session

from pages import engine
from pages.user_feedback.v1.models import Feedback, FeedbackCreate, FeedbackRead

router = APIRouter()


@router.post("/user_feedback/", response_model=FeedbackRead)
async def feedback(feedback_data: FeedbackCreate):
    feedback = Feedback(**feedback_data.dict())
    with Session(engine) as session:
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
        if feedback.id is None:
            raise HTTPException(status_code=400, detail="Feedback could not be saved")
    return feedback