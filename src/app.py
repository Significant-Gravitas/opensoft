from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.crud_module.v1.implementations.crud_module_v1_1 import crud_module_v1_router
from src.crud_module.v2.implementations.crud_module_v2_1 import crud_module_v2_router
from src.crud_module.v3.implementations.crud_module_v3_1 import crud_module_v3_router
from src.filename_replacer_v1.implementations.filename_replacer_v1_1 import filename_replacer_v1_router
from src.user_feedback_v2.implementations.user_feedback_v2_1 import feedback_router

app = FastAPI()

app.include_router(feedback_router)
app.include_router(crud_module_v1_router)
app.include_router(crud_module_v2_router)
app.include_router(crud_module_v3_router)
app.include_router(filename_replacer_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development purposes, you can use ["*"]. For production, specify your React app's origin.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
