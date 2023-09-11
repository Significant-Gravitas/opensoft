from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)


import pydevd_pycharm

pydevd_pycharm.settrace(
    "localhost", port=9739, stdoutToServer=True, stderrToServer=True
)
