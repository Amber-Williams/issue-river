from fastapi.testclient import TestClient

from app.main import app
from utils import temp_db

client = TestClient(app)

@temp_db
def test_create_user():
    response = client.post(
        "/users",
        json={
            "email": "batman@gothem.com",
            "password": "CrimeSucks33",
            "first_name": "Clark",
            "last_name": "Kent"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "batman@gothem.com",
        "first_name": "Clark",
        "last_name": "Kent",
        "is_active": True,
        "role": None,
        "workspace": None
    }