import os
import re
import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException

from pages.crud_module.v6.models import ModuleCreate, ModuleRead

router = APIRouter()


def get_all_modules() -> List[ModuleRead]:
    cwd = Path.cwd()
    modules_dir = f"{cwd}/pages"
    version_pattern = re.compile(r"^v\d+$")
    backend_pattern = re.compile(r"^b\d+$")

    # Exclude certain directories like "__pycache__"
    exclude_dirs = {"__pycache__", "crud_module"}

    modules = []
    for module_item in os.scandir(modules_dir):
        if module_item.is_dir() and module_item.name not in exclude_dirs:
            for version_item in os.scandir(module_item.path):
                if version_item.is_dir() and version_pattern.match(version_item.name):
                    for backend_item in os.scandir(version_item.path):
                        if backend_item.is_dir() and backend_pattern.match(backend_item.name):
                            modules.append(
                                ModuleRead(name=module_item.name, version=version_item.name, backend=backend_item.name)
                            )

    return sorted(
        modules, key=lambda x: (x.name.lower(), x.version, x.backend)
    )


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
    folder = f"{cwd}/pages/{module.name}"
    if not os.path.exists(folder):
        os.makedirs(folder)
        path = os.path.join(folder, "__init__.py")
        with open(path, "w") as f:
            f.write("")

    # Generate a valid version number based on module name and existence
    version_num = 1
    while os.path.exists(os.path.join(folder, f"v{version_num}")):
        version_num += 1
    version = f"v{version_num}"
    version_folder = os.path.join(folder, version)
    os.makedirs(version_folder)
    path = os.path.join(version_folder, "__init__.py")
    with open(path, "w") as f:
        f.write("")

    # Generate a valid backend number based on version and existence
    backend_num = 1
    while os.path.exists(os.path.join(version_folder, f"b{backend_num}")):
        backend_num += 1
    backend = f"b{backend_num}"
    backend_folder = os.path.join(version_folder, backend)
    os.makedirs(backend_folder)
    path = os.path.join(backend_folder, "__init__.py")
    with open(path, "w") as f:
        f.write("")

    return ModuleRead(name=module.name, version=version, backend=backend)


@router.delete("/modules/{module_name}/")
def delete_module_by_name(module_name: str):
    cwd = Path.cwd()
    module_path = f"{cwd}/pages/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)
        return {"status": "success", "message": "Module deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Module not found")
