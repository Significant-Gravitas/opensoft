# You can use an environment variable or any other mechanism to decide when to debug.
import os

import pydevd_pycharm

if os.environ.get("PYCHARM_DEBUG"):
    pydevd_pycharm.settrace(
        "localhost", port=9739, stdoutToServer=True, stderrToServer=True
    )

from importlib import import_module
from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

base_dir = Path(__file__).parent  # Now pointing to the 'src' directory
modules = [
    d.name for d in base_dir.iterdir() if d.is_dir()
]  # List all directories under 'src' as modules

import re
from importlib import import_module
from pathlib import Path

for module_name in modules:
    module_path = base_dir / module_name

    # Discover all version directories (like v1, v2, etc.)
    versions = [
        d.name for d in module_path.iterdir() if d.is_dir() and d.name.startswith("v")
    ]

    for version in versions:
        version_path = module_path / version

        # List all folders inside the version directory
        all_folders = [d for d in version_path.iterdir() if d.is_dir()]

        # Filter folders matching the regex pattern ^b\d+$
        pattern = re.compile(r"^b\d+$")
        backend_iterations = [
            folder.name for folder in all_folders if pattern.match(folder.name)
        ]

        for backend_iteration in backend_iterations:
            # Construct the dynamic import path
            dynamic_path = f"src.{module_name}.{version}.{backend_iteration}.endpoint"

            # Dynamically import the module
            module = import_module(dynamic_path)

            # Include the router in the FastAPI app
            app.include_router(
                getattr(module, "router"), prefix=f"/{version}/{backend_iteration}"
            )


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # For development purposes. For production, specify your React app's origin.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
