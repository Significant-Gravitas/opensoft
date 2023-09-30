from httpx import AsyncClient

from pages.app import app


def get_client(base_url):
    return AsyncClient(app=app, base_url=base_url)
