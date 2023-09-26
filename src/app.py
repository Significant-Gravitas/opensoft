from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from importlib import import_module
from pathlib import Path

app = FastAPI()

base_dir = Path(__file__).parent  # Now pointing to the 'src' directory
modules = [d.name for d in base_dir.iterdir() if d.is_dir()]  # List all directories under 'src' as modules

# Programmatically import and include routers
for module_name in modules:
    module_path = base_dir / module_name
    # Discover all version directories (like v1, v2, etc.)
    versions = [d.name for d in module_path.iterdir() if d.is_dir() and d.name.startswith("v")]

    for version in versions:
        # Construct the dynamic import path
        dynamic_path = f"src.{module_name}.{version}.b1.endpoint"
        if module_name not in ["module_fixture", "fixture_to_remove", "runner_pytest"]:

            # Dynamically import the module
            module = import_module(dynamic_path)

            # Include the router in the FastAPI app
            app.include_router(getattr(module, "router"), prefix=f"/{version}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development purposes. For production, specify your React app's origin.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
