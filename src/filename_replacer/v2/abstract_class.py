from pydantic import constr, BaseModel
from sqlmodel import SQLModel, Field
from typing import List

class FilenameReplacementBase(SQLModel, BaseModel):
    module_names: List[constr(min_length=1)]
    filename_contains: constr(min_length=1)
    replace_with: constr(min_length=1)

class FilenameReplacementRead(FilenameReplacementBase):
    files_replaced_before: List[str]
    files_replaced_after: List[str]

class FilenameReplacementCreate(FilenameReplacementBase):
    pass
