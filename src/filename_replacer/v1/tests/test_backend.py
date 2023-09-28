import pytest
from httpx import AsyncClient


# ...[other code]...
@pytest.mark.asyncio
async def test_can_replace_filenames_given_a_list_of_modules(client: AsyncClient):
    # Define the initial values
    module_targets = ["module_fixture"]
    filename_search = "xyz"
    filename_replacement = "def"

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

    # Updated the test to look for keys inside "data"
    assert response_data["data"]["module_names"] == module_targets
    assert response_data["data"]["filename_contains"] == filename_search
    assert response_data["data"]["replace_with"] == filename_replacement
    # reverse the operation
    response = await client.post(
        "/filename_replacement",
        json={
            "module_names": module_targets,
            "filename_contains": filename_replacement,
            "replace_with": filename_search,
        },
    )
