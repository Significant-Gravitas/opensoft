import asyncio
import pytest
from httpx import AsyncClient
from src.app import app

@pytest.fixture
def client(request):
    """
    Fixture that creates client for requesting server.

    :return: client for the app.
    """
    # Create an instance of AsyncClient
    ac = AsyncClient(app=app, base_url="http://127.0.0.1:8000")

    def fin():
        # Close the client when done
        asyncio.get_event_loop().run_until_complete(ac.aclose())

    # Use the finalizer to ensure the client is closed after usage
    request.addfinalizer(fin)

    return ac