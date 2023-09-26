import os
import shutil
from pathlib import Path

from fastapi import FastAPI, APIRouter, HTTPException
from typing import List, Union

from src.client import get_client
from src.common import print_file_content
from src.prompt_generator.v1.abstract_class import PromptRead, PromptCreate

router = APIRouter()


@router.post("/prompts", response_model=PromptRead)
async def create_filename_replacements(body: PromptCreate):
    if body.goal == "pass_tests":
        module = body.module_backend
        parts = module.rsplit('/', 1)
        module = parts[0]
        backend = parts[1]
        db_engine = print_file_content(f"src/engine.py")
        db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
        abstract_class = print_file_content(f"src/{module}/abstract_class.py")
        implementation = print_file_content(
            f"src/{module}/{backend}/endpoint.py"
        )
        fixtures = ""

        parts = module.rsplit('/', 1)
        module_name = parts[0]
        query_parameters = {
            'n': 0,
            'path': f"src/{module_name}",
        }
        client = get_client("http://localhost:8000")
        response = await client.get(
            "v1/b1/pytest_failures/",
            params=query_parameters
        )
        pytest_failure = response.json()

        # pytest_failure = RunnerPytest1().get_pytest_failure(
        #     n=int(pick_item), path=f"src/{module}"
        # )

        if pytest_failure is None:
            print("No failure found")
            pytest_failure = ""

        instructions = """
    User:
    Modify the class or the tests in order for the test to pass, depending on whether the test makes sense or not.
    Assistant:
    """
        result_str = (
            db_engine + db_hint + db_engine + abstract_class + implementation + fixtures + pytest_failure + instructions
        )

        if len(result_str) > 12000:
            result_str = db_engine + db_hint + implementation + fixtures + pytest_failure + instructions

        return PromptRead(
            module_backend=body.module_backend,
            goal=body.goal,
            prompt=result_str
        )
