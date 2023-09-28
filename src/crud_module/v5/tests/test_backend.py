import asyncio
import os

import pytest
from httpx import AsyncClient
from src.app import app  # Ensure this is the correct import path

import pytest
import shutil

@pytest.mark.asyncio
async def test_module_lifecycle(client):
    module_name = "test_module"

    # Setup: Ensure the module does not pre-exist
    module_path = f"./src/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)

    # 0. List modules before creating
    response = await client.get("/modules/")
    assert response.status_code == 200  # Assuming 200 for success
    initial_modules = response.json()
    initial_count = len(initial_modules)

    # 1. Try to get the module before creation to ensure it's not there
    response = await client.get(f"/modules/{module_name}/")
    assert response.status_code == 404  # Assuming 404 for not found

    # 2. Create the module
    module_data = {"name": module_name}
    response = await client.post("/modules/", json=module_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == module_name

    # 3. List modules after creating
    response = await client.get("/modules/")
    assert response.status_code == 200  # Assuming 200 for success
    post_creation_modules = response.json()
    post_creation_count = len(post_creation_modules)
    assert post_creation_count == initial_count + 1, f"Expected module count to increase by 1, but it increased by {post_creation_count - initial_count}"

    # 4. Try to get the module after creation to ensure it's there
    response = await client.get(f"/modules/{module_name}/")
    assert response.status_code == 200  # Assuming 200 for success
    data = response.json()
    assert data["name"] == module_name

    # 5. Delete the module
    response = await client.delete(f"/modules/{module_name}/")
    assert response.status_code == 200  # Assuming 200 for successful deletion

    # 6. Ensure it was deleted by trying to get it again
    response = await client.get(f"/modules/{module_name}/")
    assert response.status_code == 404  # Assuming 404 for not found

@pytest.mark.asyncio
async def test_default_module_listing_order(client):
    # Step: Ask for the list of modules without specifying a sort order
    response = await client.get("/modules/")
    assert response.status_code == 200  # 200 for success

    # Step: Verify that the list is sorted in ascending order
    modules_list = response.json()
    actual_order = [module["name"] for module in modules_list]

    # Check if the list is sorted in a case-insensitive manner
    assert actual_order == sorted(actual_order, key=str.lower), f"Expected the list to be sorted, but got {actual_order}"
