import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_prompt_creation(client: AsyncClient):
    response = await client.post("/prompts", json={
        "module_backend": "module_fixture/v1/b1",
        "goal": "pass_tests"
    })

    # Check the response
    assert response.status_code == 200
    response_data = response.json()

    assert "E       " in response_data["prompt"]
    assert ">       " in response_data["prompt"]

    # Updated the test to look for keys inside "data"
    # assert response_data["data"]["module_names"] == module_targets
    # assert response_data["data"]["filename_contains"] == filename_search
    # assert response_data["data"]["replace_with"] == filename_replacement
    # # reverse the operation
    # response = await client.post(
    #     "/filename_replacement",
    #     json={
    #         "module_names": module_targets,
    #         "filename_contains": filename_replacement,
    #         "replace_with": filename_search
    #     }
    # )
