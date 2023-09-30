from abc import abstractmethod

from sqlmodel import Session

from pages import engine
from pages.user_feedback_v1.models import (
    AbstractUserFeedbackV1,
    Feedback,
    FeedbackCreate,
    FeedbackRead,
    app,
)


class UserFeedbackV11(AbstractUserFeedbackV1):
    @classmethod
    def create_feedback(cls, feedback: FeedbackCreate) -> FeedbackRead:
        if not feedback.content.strip():  # Check if content is empty or just whitespace
            raise ValueError("Invalid content")

        # Create a new Feedback instance
        new_feedback = Feedback(user_id=feedback.user_id, content=feedback.content)

        with Session(engine) as session:
            # Add and commit the new feedback to the database
            session.add(new_feedback)
            session.commit()

            # Refresh the new feedback instance to get its assigned ID
            session.refresh(new_feedback)

        return FeedbackRead(
            id=new_feedback.id,
            user_id=new_feedback.user_id,
            content=new_feedback.content,
        )
