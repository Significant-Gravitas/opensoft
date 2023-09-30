# ...[other code]...
import pytest
from httpx import AsyncClient

# ...[other code]...


@pytest.mark.asyncio
async def test_can_replace_filenames_given_a_list_of_modules(client: AsyncClient):
    # Define the initial values
    module_targets = ["module_fixture"]
    filename_search = "models"
    filename_replacement = "class_abstract"

    # Send a request to the API with the improved payload
    response = await client.post(
        "/filename_replacement",
        json={
            "module_names": module_targets,
            "filename_contains": filename_search,
            "replace_with": filename_replacement,
        },
    )

    # Check the response
    assert response.status_code == 200
    response_data = response.json()

    # Asserts for data keys
    assert response_data["module_names"] == module_targets
    assert response_data["filename_contains"] == filename_search
    assert response_data["replace_with"] == filename_replacement

    # Assert for files_replaced_before and files_replaced_after
    assert "files_replaced_before" in response_data
    assert all(
        filename_search in file for file in response_data["files_replaced_before"]
    )

    # Ensure every file in files_replaced_after contains the replacement substring
    assert "files_replaced_after" in response_data
    assert all(
        filename_replacement in file for file in response_data["files_replaced_after"]
    )

    # reverse the operation
    response = await client.post(
        "/filename_replacement",
        json={
            "module_names": module_targets,
            "filename_contains": filename_replacement,
            "replace_with": filename_search,
        },
    )
