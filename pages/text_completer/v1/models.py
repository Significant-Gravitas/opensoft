from pydantic import constr
from sqlmodel import SQLModel, Field


class TextCompletionBase(SQLModel):
    # The regex here checks for names that end with _v followed by one or more digits
    input: str


class TextCompletionRead(TextCompletionBase):
    id: int
    output: str

class TextCompletionCreate(TextCompletionBase):
    pass

class TextCompletion(TextCompletionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    output: str = Field(default=None)
