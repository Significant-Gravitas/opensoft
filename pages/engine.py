from sqlalchemy import create_engine
from sqlmodel import SQLModel

from pages.user_feedback.v1 import models
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)
