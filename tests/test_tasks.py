import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a FastAPI client for testing."""
    from app import app
    return TestClient(app)


def test_delete_task(client):
    """Test the delete_task endpoint."""
    # Test deleting a task that exists
    response = client.delete("/tasks/123")
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # Test deleting a task that does not exist
    response = client.delete("/tasks/123")
    assert response.status_code == 404
    assert response.json() == {"success": False, "error": "Item not found"}