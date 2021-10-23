from fastapi.testclient import TestClient

from app.main import app
from utils import temp_db

client = TestClient(app)

workspace = {
    "name": "Get shit done Inc."
}

user = {
    "email": "batman@gothem.com",
    "password": "CrimeSucks33",
    "first_name": "Clark",
    "last_name": "Kent"
}

user2 = {
    "email": "robin@gothem.com",
    "password": "BatmanRocks1234",
    "first_name": "Robin",
    "last_name": "Hood"
}

def create_user(user):
    return client.post(
        "/user",
        json=user,
    )

def read_user(id: int):
    return client.get(f"/user/{id}")

def create_workspace():
    return client.post(
        "/workspace",
        json={
            "name": workspace["name"],
            "user_id": 1
        },
    )

def read_workspace(id: int):
    return client.get(f"/workspace/{id}")

def add_user_to_workspace(id: int, user_id: int):
    return client.put(
        "/workspace/user",
        json={
            "id": id,
            "user_id": user_id
        },
    )

def remove_user_from_workspace(id: int, user_id: int):
    return client.delete(
        "/workspace/user",
        json={
            "id": id,
            "user_id": user_id
        },
    )

@temp_db
def test_create_and_get_user():
    expected = {
        "id": 1,
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "is_active": True,
        "role": None,
        "workspace": None
    }
    response = create_user(user)
    assert response.status_code == 200
    assert response.json() == expected
    response = read_user(1)
    assert response.status_code == 200
    assert response.json() == expected

@temp_db
def test_create_and_get_workspace():
    expected = {
        "id": 1,
        "name": "Get shit done Inc.",
        "is_active": True,
        "users": [
            {
            "id": 1,
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "is_active": True,
            "role": None,
            "workspace": 1
            }
        ]
    }
    create_user(user)
    response = create_workspace()
    assert response.status_code == 200
    assert response.json() == expected
    response = read_workspace(1)
    assert response.status_code == 200
    assert response.json() == expected


@temp_db
def test_multiuser_workspace():
    create_user(user)
    response =create_workspace()
    assert response.status_code == 200
    assert len(response.json()['users']) == 1
    create_user(user2)
    response = add_user_to_workspace(id=1, user_id=2)
    assert response.status_code == 200
    assert len(response.json()['users']) == 2
    response = remove_user_from_workspace(id=1, user_id=2)
    assert response.status_code == 200
    assert len(response.json()['users']) == 1
