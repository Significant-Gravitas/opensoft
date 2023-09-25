import os
import shutil
from pathlib import Path

from fastapi import FastAPI, APIRouter, HTTPException
from typing import List
from src.file_renamer_v1.abstract_class import ModuleCreate, ModuleRead

file_renamer_v1_router = APIRouter()

def get_all_modules():
    cwd = Path.cwd()
    modules_dir = f"{cwd}/src"

    # Exclude certain directories like "__pycache__"
    exclude_dirs = {"__pycache__"}

    modules = [ModuleRead(name=item.name) for item in os.scandir(modules_dir) if item.is_dir() and item.name not in exclude_dirs]
    return sorted(modules, key=lambda x: x.name.lower())  # Ensure sorting is case-insensitive



@file_renamer_v1_router.get("/v1/modules/")
def get_modules() -> List[ModuleRead]:
    return get_all_modules()

@file_renamer_v1_router.get("/v1/modules/{module_name}/")
def get_module_by_name(module_name: str) -> ModuleRead:
    all_modules = get_all_modules()
    if module_name not in [module.name for module in all_modules]:
        raise HTTPException(status_code=404, detail="Module not found")
    return ModuleRead(name=module_name)

@file_renamer_v1_router.post("/v1/modules/", response_model=ModuleRead)
def create_module(module: ModuleCreate) -> dict:
    cwd = Path.cwd()
    folder = f"{cwd}/src/{module.name}"
    if not os.path.exists(folder):
        os.makedirs(folder)
        path = os.path.join(folder, "__init__.py")
        with open(path, 'w') as f:
            f.write("")
    return ModuleRead(name=module.name)

@file_renamer_v1_router.delete("/v1/modules/{module_name}/")
def delete_module_by_name(module_name: str):
    cwd = Path.cwd()
    module_path = f"{cwd}/src/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)
        return {"status": "success", "message": "Module deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Module not found")
