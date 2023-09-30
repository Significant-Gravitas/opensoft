import json
from typing import Optional

from fastapi import APIRouter

# from pages.runner_pytest.models import AbstractRunnerPytest

router = APIRouter()


from fastapi import Query


@router.get("/pytest_failures/")
def get_pytest_failures(n: int = Query(...), path: Optional[str] = None):
    import subprocess

    command = ["pytest", path, "--json-report", "--mock"]

    result = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    with open(".report.json", "r") as f:
        data = json.load(f)
    result = get_nth_failure_longrepr(n, data)

    return result


def get_nth_failure_longrepr(n, test_data):
    failed_tests = [test for test in test_data["tests"] if test["outcome"] == "failed"]
    if n < len(failed_tests):
        call = failed_tests[n]["call"]
        crash = json.dumps(call["crash"], indent=4, sort_keys=True)
        traceback = json.dumps(call["traceback"][0], indent=4, sort_keys=True)
        message = crash + traceback

        return message
    else:
        return None
