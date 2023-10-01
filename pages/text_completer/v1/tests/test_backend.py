import pytest

from pages.app import app  # Ensure this is the correct import path

@pytest.mark.vcr(record_mode='new_episodes')
@pytest.mark.asyncio
async def test_text_completion_lifecycle_with_capital(client):
    input_text = "What's the capital of America?"

    # 1. Create a new TextCompletion
    completion_data = {"input": input_text}
    response = await client.post("/text_completions/", json=completion_data)
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == input_text
    assert "washington" in data["output"].lower()  # Expecting the output to contain "washington"
    completion_id = data["id"]

    # 2. Read the TextCompletion back by its ID
    response = await client.get(f"/text_completions/{completion_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == input_text and "output" in data
    assert "washington" in data["output"].lower()  # Verifying again that the output contains "washington"

    # 3. Read a list of TextCompletions to ensure the newly created one is in the list
    response = await client.get("/text_completions/")
    assert response.status_code == 200
    completions_list = response.json()
    assert completions_list, "The list of completions is empty."
    assert any(completion["input"] == input_text for completion in completions_list)
