import os
import shutil

import pytest

from pages.app import app  # Ensure this is the correct import path


@pytest.mark.asyncio
async def test_module_lifecycle(client):
    module_name = "test_module"

    # Setup: Ensure the module does not pre-exist
    module_path = f"./pages/{module_name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)
    

    # 0. List modules before creating
    response = await client.get(f"/modules/?name={module_name}")
    assert response.status_code == 200
    modules = response.json()
    assert not modules, f"Expected no modules named {module_name}, but found some."

    # 1. Create the module
    module_data = {"name": module_name}
    response = await client.post("/modules/", json=module_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == module_name
    assert data["version"].startswith("v")

    # 2. List modules after creating
    response = await client.get(f"/modules/?name={module_name}")
    assert response.status_code == 200
    modules_after_creation = response.json()
    assert modules_after_creation, f"Expected modules named {module_name}, but found none."

    # 3. Delete the module
    response = await client.delete(f"/modules/{module_name}/")
    assert response.status_code == 200

    # 4. Ensure it was deleted by trying to list it again
    response = await client.get(f"/modules/?name={module_name}")
    assert response.status_code == 200
    modules_after_deletion = response.json()
    assert not modules_after_deletion, f"Expected no modules named {module_name}, but found some."


@pytest.mark.asyncio
async def test_default_module_listing_order(client):
    module_name = "test_module"

    # Step 1: Create the module named 'test_module'
    module_data = {"name": module_name}
    create_response = await client.post("/modules/", json=module_data)
    assert create_response.status_code == 200

    # Step 2: Ask for the list of modules specifying the name as a query parameter
    response = await client.get(f"/modules/?name={module_name}")
    assert response.status_code == 200

    # Step 3: Verify that the list has the expected module
    modules_list = response.json()
    assert any(module["name"] == module_name for module in modules_list), f"Expected to find a module named {module_name}, but didn't."

    # Cleanup: Remove the module after the test
    await client.delete(f"/modules/{module_name}/")
