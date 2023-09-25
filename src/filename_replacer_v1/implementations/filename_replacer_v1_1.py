import os
import shutil
from pathlib import Path

from fastapi import FastAPI, APIRouter, HTTPException
from typing import List

from src.filename_replacer_v1.abstract_class import FilenameReplacementRead

filename_replacer_v1_router = APIRouter()

def get_all_modules():
    cwd = Path.cwd()
    modules_dir = f"{cwd}/src"

    # Exclude certain directories like "__pycache__"
    exclude_dirs = {"__pycache__"}

    modules = [FileReplacementRead(name=item.name) for item in os.scandir(modules_dir) if item.is_dir() and item.name not in exclude_dirs]
    return sorted(modules, key=lambda x: x.name.lower())  # Ensure sorting is case-insensitive



@filename_replacer_v1_router.get("/v1/filename_replacements/")
def get_modules() -> List[FilenameReplacementRead]:
    pass
