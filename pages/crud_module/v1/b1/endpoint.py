import os
import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException

from pages.crud_module.v1.models import ModuleCreate, ModuleRead

router = APIRouter()


def get_all_modules():
    cwd = Path.cwd()
    modules_dir = f"{cwd}/pages"
    return [
        ModuleRead(name=item.name) for item in os.scandir(modules_dir) if item.is_dir()
    ]


@router.get("/modules/")
def get_modules() -> List[ModuleRead]:
    return get_all_modules()


@router.get("/modules/{module_name}/")
def get_module_by_name(module_name: str) -> ModuleRead:
    all_modules = get_all_modules()
    if module_name not in [module.name for module in all_modules]:
        raise HTTPException(status_code=404, detail="Module not found")
    return ModuleRead(name=module_name)


@router.post("/modules/", response_model=ModuleRead)
def create_module(module: ModuleCreate) -> dict:
    cwd = Path.cwd()
    folder = f"{cwd}/pages/{module.name}"
    if not os.path.exists(folder):
        os.makedirs(folder)
        path = os.path.join(folder, "__init__.py")
        with open(path, "w") as f:
            f.write("")
    return ModuleRead(name=module.name)


@router.delete("/modules/{module_name}/")
def delete_module_by_name(module_name: str):
    cwd = Path.cwd()
    module_path = f"{cwd}/pages/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)
        return {"status": "success", "message": "Module deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Module not found")
