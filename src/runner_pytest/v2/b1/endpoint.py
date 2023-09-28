import json
import re
from typing import Optional

from fastapi import APIRouter


# from src.runner_pytest.models import AbstractRunnerPytest

router = APIRouter()


from fastapi import Query


@router.get("/pytest_failures/")
def get_pytest_failures(n: int = Query(...), path: Optional[str] = None):
    import subprocess

    command = ["pytest", path, "--json-report", "--mock"]

    result = subprocess.run(command)
    with open(".report.json", "r") as f:
        data = json.load(f)
    result = get_nth_failure_longrepr(n, data)

    return remove_content_between_delimiters(
        result,
        "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    )


def remove_content_between_delimiters(text, delimiter):
    pattern = re.escape(delimiter) + ".*?" + re.escape(delimiter)
    return re.sub(pattern, delimiter + delimiter, text, flags=re.DOTALL)


def get_nth_failure_longrepr(n, test_data):
    failed_tests = [test for test in test_data["tests"] if test["outcome"] == "failed"]
    if n < len(failed_tests):
        return failed_tests[n]["call"]["longrepr"]
    else:
        return None
