from pydantic import constr
from sqlmodel import Field, SQLModel


# Define a class for creating feedback
class ChangeMeBase(SQLModel):
    user_id: int


class ChangeMeRead(ChangeMeBase):
    id: int


class ChangeMeCreate(ChangeMeBase):
    pass


class ChangeMe(ChangeMeBase, table=True):
    id: int = Field(default=None, primary_key=True)
