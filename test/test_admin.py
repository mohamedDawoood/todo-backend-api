from starlette import status
from .utils import client, test_todo, override_get_db
from main import app
from routers.auth import get_db, is_admin

app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[is_admin] = lambda: {"username": "Dawod", "id": 1, "role": "admin"}


def test_admin_read_all(test_todo):
    response = client.get("/admin/todo")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [{
        "owner_id": 1,
        "title": "learn testing",
        "description": "learning testing",
        "priority": 1,
        "complete": False,
        "id": 1
    }]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT