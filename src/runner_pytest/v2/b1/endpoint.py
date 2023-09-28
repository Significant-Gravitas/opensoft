import json
import os
import re
import sys
from contextlib import contextmanager
from typing import List, Optional, Tuple

import pytest
from fastapi import APIRouter

from src.runner_pytest.v1.models import AbstractRunnerPytest, PytestFailureRead

# from src.runner_pytest.models import AbstractRunnerPytest

router = APIRouter()


from fastapi import Query

@router.get("/pytest_failures/")
def get_pytest_failures(n: int = Query(...), path: Optional[str] = None):
    import subprocess

    command = ["pytest", "--json-report", "-v", path, "--mock"]

    result = subprocess.run(command, capture_output=True, text=True)
    with open(".report.json", "r") as f:
        data = json.load(f)
    result = get_nth_failure_longrepr(n, data)
    return result

def get_nth_failure_longrepr(n, test_data):
    failed_tests = [test for test in test_data['tests'] if test['outcome'] == 'failed']
    if n < len(failed_tests):
        return failed_tests[n]['call']['longrepr']
    else:
        return None
