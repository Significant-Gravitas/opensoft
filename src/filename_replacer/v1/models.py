from typing import List

from pydantic import BaseModel, constr
from sqlmodel import SQLModel


class FilenameReplacementBase(SQLModel, BaseModel):
    module_names: List[constr(min_length=1)]
    filename_contains: constr(min_length=1)
    replace_with: constr(min_length=1)


class FilenameReplacementRead(FilenameReplacementBase):
    pass


class FilenameReplacementCreate(FilenameReplacementBase):
    pass
