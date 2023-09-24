import pytest
import asyncio

@pytest.mark.asyncio
async def test_submitting_feedback(client):
    data = {
        "user_id": 1,
        "content": "This is a valid feedback"
    }

    # Using the request method to send the POST request.
    response = await client.post("/feedback/", json=data) # Add the trailing slash

    # Assertions
    assert response.status_code == 200

import pytest

@pytest.mark.asyncio
async def test_submitting_feedback_with_invalid_content(client):
    data = {
        "user_id": 1,
        "content": ""  # Empty content to simulate invalid feedback
    }

    # Using the request method to send the POST request.
    response = await client.post("/feedback/", json=data)  # Ensure the trailing slash

    # Assertions
    assert response.status_code != 200  # The status code should not be 200, as it's an error
    assert "ensure this value has at least 1 characters" in response.text
