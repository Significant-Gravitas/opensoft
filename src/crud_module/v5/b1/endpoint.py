import os
import re
import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException

from src.crud_module.v5.models import ModuleCreate, ModuleRead

router = APIRouter()


def get_all_modules():
    cwd = Path.cwd()
    modules_dir = f"{cwd}/src"
    version_pattern = re.compile(r"^v\d+$")

    # Exclude certain directories like "__pycache__"
    exclude_dirs = {"__pycache__"}

    modules = []
    for module_item in os.scandir(modules_dir):
        if module_item.is_dir() and module_item.name not in exclude_dirs:
            for version_item in os.scandir(module_item.path):
                if version_item.is_dir() and version_pattern.match(
                    version_item.name
                ):  # Ensure version conforms to pattern
                    modules.append(
                        ModuleRead(name=module_item.name, version=version_item.name)
                    )

    return sorted(
        modules, key=lambda x: (x.name.lower(), x.version)
    )  # Ensure sorting is by module name and then by version


@router.get("/modules/")
def get_modules() -> List[ModuleRead]:
    return get_all_modules()


@router.get("/modules/{module_name}/")
def get_module_by_name(module_name: str) -> ModuleRead:
    all_modules = get_all_modules()
    for module in all_modules:
        if module.name == module_name:
            return module
    raise HTTPException(status_code=404, detail="Module not found")


@router.post("/modules/", response_model=ModuleRead)
def create_module(module: ModuleCreate) -> dict:
    cwd = Path.cwd()
    folder = f"{cwd}/src/{module.name}"
    if not os.path.exists(folder):
        os.makedirs(folder)
        path = os.path.join(folder, "__init__.py")
        with open(path, "w") as f:
            f.write("")
    # Generate a valid version number based on module name and existence
    # Example: If "v1" exists for a module, then "v2" is created, and so on.
    version_num = 1
    while os.path.exists(os.path.join(folder, f"v{version_num}")):
        version_num += 1
    version = f"v{version_num}"
    version_folder = os.path.join(folder, version)
    os.makedirs(version_folder)
    path = os.path.join(version_folder, "__init__.py")
    with open(path, "w") as f:
        f.write("")
    return ModuleRead(name=module.name, version=version)


@router.delete("/modules/{module_name}/")
def delete_module_by_name(module_name: str):
    cwd = Path.cwd()
    module_path = f"{cwd}/src/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)
        return {"status": "success", "message": "Module deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Module not found")
