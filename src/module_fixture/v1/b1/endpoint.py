from fastapi import APIRouter

from src.module_fixture.v1.abstract_class import AbstractModuleFixture

router = APIRouter()

class ModuleFixture1(AbstractModuleFixture):
    pass
