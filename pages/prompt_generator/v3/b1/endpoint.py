from fastapi import APIRouter

from pages.common import print_file_content
from pages.prompt_generator.v3.models import PromptCreate, PromptRead

router = APIRouter()


@router.post("/prompts", response_model=PromptRead)
async def create_prompts(body: PromptCreate):
    from pages.client import get_client
    parts = body.module_backend.rsplit("/", 2)
    module_name = parts[0]
    module_version = parts[1]
    backend_iteration = parts[2]
    result_str = ""
    models = print_file_content(f"pages/{module_name}/{module_version}/models.py")

    test = print_file_content(
        f"pages/{module_name}/{module_version}/tests/test_backend.py"
    )
    if body.goal == "pass_tests":
        db_engine = print_file_content(f"pages/engine.py")
        db_hint = "To use the db:\n with Session(engine) as session:\n    pass"
        implementation = print_file_content(
            f"pages/{module_name}/{module_version}/{backend_iteration}/endpoint.py"
        )

        fixtures = ""

        query_parameters = {
            "n": 0,
            "path": f"pages/{module_name}",
        }
        client = get_client("http://localhost:8000")
        response = await client.get(f"v2/b1/pytest_failures/", params=query_parameters)
        pytest_failure = response.json()

        if pytest_failure is None or not pytest_failure:
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
    elif body.goal == "pass_frontend_tests":
      instructions = "Please make the tests pass by changing the tests or changing the component"
      component = print_file_content(
          f"pages/{module_name}/{module_version}/component.test.tsx"
      )
      component_test = print_file_content(
          f"pages/{module_name}/{module_version}/component.test.tsx"
      )
      result_str = (
        models
        + test
        + component
        + component_test
        + instructions
      )
    from fastapi import HTTPException

    if not result_str or result_str.isspace():
        raise HTTPException(status_code=400, detail="Result is empty or invalid")


    return PromptRead(
        module_backend=body.module_backend, goal=body.goal, prompt=result_str
    )
