

from src.engine import engine


# import pydevd_pycharm
#
#
# pydevd_pycharm.settrace(
#     "localhost", port=9739, stdoutToServer=True, stderrToServer=True
# )
# from abc import ABC, abstractmethod
# from typing import Any
#
# from sqlmodel import SQLModel, Field
#
# from src.base_class import BaseClass
#
# # Define a class for creating feedback
# class FeedbackBase(SQLModel):
#     user_id: int
#     content: str
#
# class FeedbackRead(FeedbackBase):
#     id: int
#
# class FeedbackCreate(FeedbackBase):
#     pass
#
# class Feedback(
#     FeedbackBase,
#     table=True
# ):
#     id: int = Field(default=None, primary_key=True)
#
# class AbstractUserFeedbackV1(ABC, BaseClass):
#
#     @classmethod
#     @abstractmethod
#     def create_feedback(cls, feedback: FeedbackCreate):
#         pass
