import os
import shutil
from pathlib import Path
from typing import List, Union

from fastapi import APIRouter

from src.filename_replacer.v1.models import (
    FilenameReplacementCreate,
    FilenameReplacementRead,
)

router = APIRouter()


def rename_files_in_modules(
    module_names: List[str], filename_contains: str, replace_with: str
):
    cwd = Path.cwd()
    modules_dir = Path(f"{cwd}/src")  # Convert string to a Path object

    for module in module_names:
        module_path = modules_dir / module

        if module_path.exists() and module_path.is_dir():
            for item in os.scandir(module_path):
                if item.is_file() and filename_contains in item.name:
                    new_name = item.name.replace(filename_contains, replace_with)
                    shutil.move(item.path, module_path / new_name)


@router.post(
    "/filename_replacement", response_model=Union[FilenameReplacementRead, dict]
)
async def create_filename_replacements(replacement: FilenameReplacementCreate):
    # Execute filename replacements
    rename_files_in_modules(
        replacement.module_names,
        replacement.filename_contains,
        replacement.replace_with,
    )

    return {"data": replacement, "message": "Success"}
