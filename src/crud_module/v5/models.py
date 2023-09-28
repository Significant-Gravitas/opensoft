from pydantic import constr
from sqlmodel import SQLModel


# Define a class for creating feedback
def snake_case_validator(name: str) -> str:
    if name != "_".join(word.lower() for word in name.split("_")):
        raise ValueError("Module name is not in snake case")
    return name


class ModuleBase(SQLModel):
    # The regex here checks for names that end with _v followed by one or more digits
    name: constr(min_length=1)


class ModuleRead(ModuleBase):
    version: constr(regex=r"^v\d+$", min_length=2)


class ModuleCreate(ModuleBase):
    pass


class ModuleCreate(ModuleBase):
    pass


# the following acts as an contract for the routes

# @app.post("/modules/", response_model=ModuleRead)
# def get_modules(feedback: ModuleCreate):
#     pass
