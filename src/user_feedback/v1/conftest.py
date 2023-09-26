import pytest
from httpx import AsyncClient
import asyncio

from src.app import app

from pathlib import Path

from src.utils import get_backend_iterations


@pytest.fixture(params=get_backend_iterations(Path(__file__).parent))
def client(request):
    """
    Fixture that creates client for requesting server based on different base URLs.

    :return: client for the app.
    """
    base_url = request.param  # Retrieve the current parameter

    # Create an instance of AsyncClient with the parameterized base URL
    ac = AsyncClient(app=app, base_url=base_url)

    def fin():
        # Close the client when done
        asyncio.get_event_loop().run_until_complete(ac.aclose())

    # Use the finalizer to ensure the client is closed after usage
    request.addfinalizer(fin)

    return ac
