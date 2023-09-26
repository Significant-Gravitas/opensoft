import os
import shutil
from pathlib import Path

from fastapi import FastAPI, APIRouter, HTTPException
from typing import List, Union

from src.filename_replacer.v1.abstract_class import FilenameReplacementCreate, FilenameReplacementRead

router = APIRouter()

def rename_files_in_modules(module_names: List[str], filename_contains: str, replace_with: str) -> (List[str], List[str]):
    cwd = Path.cwd()
    modules_dir = Path(f"{cwd}/src")  # Convert string to a Path object

    files_before = []
    files_after = []

    for module in module_names:
        module_path = modules_dir / module

        if module_path.exists() and module_path.is_dir():
            for item in os.scandir(module_path):
                if item.is_file() and filename_contains in item.name:
                    new_name = item.name.replace(filename_contains, replace_with)
                    files_before.append(item.name)
                    files_after.append(new_name)
                    shutil.move(item.path, module_path / new_name)

    return files_before, files_after



@router.post("/filename_replacement", response_model=FilenameReplacementRead)
async def create_filename_replacements(replacement: FilenameReplacementCreate):
    # Execute filename replacements and gather the lists of filenames before and after
    files_before, files_after = rename_files_in_modules(replacement.module_names, replacement.filename_contains, replacement.replace_with)

    # Ensure the keys are always present in the response data
    return {
        "module_names": replacement.module_names,
        "filename_contains": replacement.filename_contains,
        "replace_with": replacement.replace_with,
        "files_replaced_before": files_before or [],
        "files_replaced_after": files_after or []
    }
