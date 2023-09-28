
from fastapi import APIRouter

from src.common import print_file_content
from src.prompt_generator.v1.models import PromptCreate, PromptRead

router = APIRouter()


@router.post("/prompts", response_model=PromptRead)
async def create_filename_replacements(body: PromptCreate):
    from src.client import get_client

    if body.goal == "pass_tests":
        parts = body.module_backend.rsplit("/", 2)
        module_name = parts[0]
        module_version = parts[1]
        backend_iteration = parts[2]
        db_engine = print_file_content(f"src/engine.py")
        db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
        models = print_file_content(f"src/{module_name}/{module_version}/models.py")
        implementation = print_file_content(
            f"src/{module_name}/{module_version}/{backend_iteration}/endpoint.py"
        )
        test = print_file_content(
            f"src/{module_name}/{module_version}/tests/test_backend.py"
        )
        fixtures = ""

        query_parameters = {
            "n": 0,
            "path": f"src/{module_name}",
        }
        client = get_client("http://localhost:8000")
        response = await client.get(f"v2/b1/pytest_failures/", params=query_parameters)
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
            db_engine
            + db_hint
            + db_engine
            + models
            + implementation
            + fixtures
            + test
            + pytest_failure
            + instructions
        )

        if len(result_str) > 12000:
            result_str = (
                db_engine
                + db_hint
                + implementation
                + fixtures
                + test
                + pytest_failure
                + instructions
            )

        return PromptRead(
            module_backend=body.module_backend, goal=body.goal, prompt=result_str
        )
