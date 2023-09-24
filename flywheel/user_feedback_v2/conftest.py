import pytest
from httpx import AsyncClient

from flywheel.app import app


@pytest.fixture
async def client(
    anyio_backend,
):
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(
            app=app,
            base_url="http://127.0.0.1:8000"
    ) as ac:
        yield ac
