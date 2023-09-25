from pydantic import constr
from sqlmodel import SQLModel, Field


# Define a class for creating feedback
class FilenameReplacementBase(SQLModel):
    name: constr(min_length=1)

class FilenameReplacementRead(FilenameReplacementBase):
    pass
class FilenameReplacementCreate(FilenameReplacementBase):
    pass
