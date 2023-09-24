from pydantic import constr
from sqlmodel import SQLModel, Field


# Define a class for creating feedback
class ModuleBase(SQLModel):
    name: constr(min_length=1)

class ModuleRead(ModuleBase):
    pass
class ModuleCreate(ModuleBase):
    pass

# the following acts as an contract for the routes

# @app.post("/modules/", response_model=ModuleRead)
# def get_modules(feedback: ModuleCreate):
#     pass
