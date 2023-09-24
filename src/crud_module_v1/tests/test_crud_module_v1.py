import asyncio
import os

import pytest
from httpx import AsyncClient
from src.app import app  # Ensure this is the correct import path

@pytest.mark.asyncio
async def test_listing_modules(client):
    response = await client.get("/modules/")
    assert response.status_code == 200
    data = response.json()
    assert "modules" in data
    assert isinstance(data["modules"], list)

import pytest
from httpx import AsyncClient
from src.app import app  # Ensure this is the correct import path

import shutil

@pytest.mark.asyncio
async def test_module_lifecycle(client):
    module_name = "test_module"

    # Setup: Ensure the module does not pre-exist
    module_path = f"./src/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)

    # 1. Try to get the module before creation to ensure it's not there
    response = await client.get(f"/modules/{module_name}/")
    assert response.status_code == 404  # Assuming 404 for not found
    # 2. Create the module
    module_data = {"name": module_name}
    response = await client.post("/modules/", json=module_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == module_name

    # 3. Try to get the module after creation to ensure it's there
    response = await client.get(f"/modules/{module_name}/")
    assert response.status_code == 200  # Assuming 200 for success
    data = response.json()
    assert data["name"] == module_name

    # 4. Delete the module
    response = await client.delete(f"/modules/{module_name}/")
    assert response.status_code == 200  # Assuming 200 for successful deletion

    # 5. Ensure it was deleted by trying to get it again
    response = await client.get(f"/modules/{module_name}/")
    assert response.status_code == 404  # Assuming 404 for not found
