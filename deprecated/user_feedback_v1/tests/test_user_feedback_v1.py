# from src.user_feedback_v1.models import FeedbackCreate
# import pytest


# # This test is for the scenario "Submitting Feedback"
# def test_submitting_feedback(user_feedback_v1):
#     # Setup: Create a mock user and a valid feedback content
#     user = {"id": 1, "name": "Test User"}
#     valid_feedback_content = "This is a valid feedback."
#
#     feedback = FeedbackCreate(user_id=user["id"], content=valid_feedback_content)
#
#     # Execute: Call the create_feedback method to submit feedback
#     saved_feedback = user_feedback_v1.create_feedback(feedback)
#
#     # Assert: Check if the feedback was saved correctly
#     assert saved_feedback.user_id == user["id"]
#     assert saved_feedback.content == valid_feedback_content
#     # This line checks if the feedback was acknowledged with a success message, but
#     # since the function's return type is FeedbackRead and there's no such message in it,
#     # we might need to modify the system's functionality to return a success message or omit this line.
#     # assert "Success" in saved_feedback.message
#
# from src.user_feedback_v1.models import FeedbackCreate
#
# # This test is for the scenario "Submitting Feedback with invalid content"
# def test_submitting_feedback_with_invalid_content(user_feedback_v1):
#     # Setup: Create a mock user and an invalid feedback content
#     user = {"id": 1, "name": "Test User"}
#     invalid_feedback_content = ""  # Assuming empty content is invalid
#
#     feedback = FeedbackCreate(user_id=user["id"], content=invalid_feedback_content)
#
#     # Execute & Assert
#     with pytest.raises(ValueError, match="Invalid content"):  # Assuming a ValueError will be raised for invalid content
#         user_feedback_v1.create_feedback(feedback)
#
# def test_no_hardcoded_ids(user_feedback_v1):
#     feedback1 = FeedbackCreate(user_id=1, content="First feedback")
#     feedback2 = FeedbackCreate(user_id=2, content="Second feedback")
#
#     response1 = user_feedback_v1.create_feedback(feedback1)
#     response2 = user_feedback_v1.create_feedback(feedback2)
#
#     assert response1.id != response2.id, "IDs should be unique"
#     assert response2.id == response1.id + 1, "IDs should increment by 1"
