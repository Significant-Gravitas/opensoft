from fastapi import APIRouter
from sqlmodel import Session

from pages import engine
from pages.user_feedback.v1.models import Feedback, FeedbackCreate, FeedbackRead

router = APIRouter()


@router.post("/user_feedback/", response_model=FeedbackRead)
async def feedback(feedback_data: FeedbackCreate):
    # Initialize a session with the engine
    with Session(engine) as session:
        # Create a new feedback instance with the data
        feedback = Feedback(user_id=feedback_data.user_id, content=feedback_data.content)

        # Add the feedback instance to the session
        session.add(feedback)

        # Commit the transaction to save the feedback in the database
        session.commit()

        # Refresh the feedback instance to get the newly generated ID
        session.refresh(feedback)

        # Return the feedback instance
        return feedback
