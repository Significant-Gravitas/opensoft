import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_prompt_creation(client: AsyncClient):
    response = await client.post(
        "/prompts",
        json={"module_backend": "module_fixture/v1/b1", "goal": "pass_tests"},
    )

    # Check the response
    assert response.status_code == 200
    response_data = response.json()
    # TODO: put this back when we use runner_pytest/v1
    # assert "E       " in response_data["prompt"]
    # assert ">       " in response_data["prompt"]
