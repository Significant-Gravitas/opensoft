from fastapi import APIRouter
from sqlmodel import Session

from pages import engine
from pages.change_me.v1.models import ChangeMe, ChangeMeCreate, ChangeMeRead

router = APIRouter()


@router.post("/change_mes/", response_model=ChangeMeRead)
async def create_change_mes(body: ChangeMeCreate):
    pass
