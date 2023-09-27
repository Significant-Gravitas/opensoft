from fastapi import APIRouter

from src.module_fixture.v1.models import AbstractModuleFixture

router = APIRouter()

class ModuleFixture1(AbstractModuleFixture):
    pass
