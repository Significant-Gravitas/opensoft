from fastapi import APIRouter

from pages.module_fixture.v1.models import AbstractModuleFixture

router = APIRouter()


class ModuleFixture1(AbstractModuleFixture):
    pass
