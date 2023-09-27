from pydantic import constr, validator
from sqlmodel import SQLModel, Field


# Define a class for creating feedback
def snake_case_validator(name: str) -> str:
    if name != "_".join(word.lower() for word in name.split("_")):
        raise ValueError("Module name is not in snake case")
    return name

class ModuleBase(SQLModel):
    # The regex here checks for names that end with _v followed by one or more digits
    name: constr(min_length=1)

    # name: constr(regex=r'.*_v\d+$', min_length=1) = ...
    #
    # @validator("name", pre=True, always=True)
    # def validate_snake_case(cls, name):
    #     return snake_case_validator(name)

class ModuleRead(ModuleBase):
    pass

class ModuleCreate(ModuleBase):
    pass

class ModuleRead(ModuleBase):
    pass
class ModuleCreate(ModuleBase):
    pass



# the following acts as an contract for the routes

# @app.post("/modules/", response_model=ModuleRead)
# def get_modules(feedback: ModuleCreate):
#     pass
