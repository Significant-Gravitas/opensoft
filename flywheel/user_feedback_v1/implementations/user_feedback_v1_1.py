from abc import abstractmethod

from flywheel import engine
from flywheel.user_feedback_v1.abstract_class import AbstractUserFeedbackV1, FeedbackCreate, FeedbackRead, Feedback, app

from sqlmodel import Session
from flywheel.user_feedback_v1.abstract_class import AbstractUserFeedbackV1, FeedbackCreate, FeedbackRead




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

        return FeedbackRead(id=new_feedback.id, user_id=new_feedback.user_id, content=new_feedback.content)
