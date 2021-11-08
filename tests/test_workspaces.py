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

class TestWorkspaces:
    def __init__(self):
        self.access_token = None

    def create_user(self, user):
        return client.post(
            "/user",
            json=user,
        )

    def login_user(self, user):
        return client.post("/login", data={"username": user["email"], "password": user["password"]}, headers={"content-type": "application/x-www-form-urlencoded"})

    def read_user(self, id: int):
        return client.get(f"/user/{id}", headers={"Authorization": f"Bearer {self.access_token}"})

    def create_workspace(self):
        return client.post(
            "/workspace",
            json={
                "name": workspace["name"],
                "user_id": 1
            },
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

    def read_workspace(self, id: int):
        return client.get(f"/workspace/{id}", headers={"Authorization": f"Bearer {self.access_token}"})

    def add_user_to_workspace(self, id: int, user_id: int):
        return client.put(
            "/workspace/user",
            json={
                "id": id,
                "user_id": user_id
            },
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

    def remove_user_from_workspace(self, id: int, user_id: int):
        return client.delete(
            "/workspace/user",
            json={
                "id": id,
                "user_id": user_id
            },
            headers={"Authorization": f"Bearer {self.access_token}"}
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
    w = TestWorkspaces()
    response = w.create_user(user)
    assert response.status_code == 200
    assert response.json() == expected
    response = w.login_user(user)
    w.access_token = response.json()["access_token"]
    response = w.read_user(1)
    assert response.status_code == 200
    assert response.json() == expected

@temp_db
def test_create_and_get_workspace():
    expected = {
        "id": 1,
        "name": workspace["name"],
        "users": [
            {
            "id": 1,
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "is_active": True,
            "role": "owner",
            "workspace": 1
            }
        ]
    }
    w = TestWorkspaces()
    w.create_user(user)
    response = w.login_user(user)
    w.access_token = response.json()["access_token"]
    response = w.create_workspace()
    assert response.status_code == 200
    assert response.json() == expected
    response = w.read_workspace(1)
    assert response.status_code == 200
    assert response.json() == expected


@temp_db
def test_multiuser_workspace():
    w1 = TestWorkspaces()
    w1.create_user(user)
    response = w1.login_user(user)
    w1.access_token = response.json()["access_token"]
    response = w1.create_workspace()
    assert response.status_code == 200
    assert len(response.json()['users']) == 1

    w2 = TestWorkspaces()
    w2.create_user(user2)
    response = w1.add_user_to_workspace(id=1, user_id=2)
    assert response.status_code == 200
    assert len(response.json()['users']) == 2
    response = w1.remove_user_from_workspace(id=1, user_id=2)
    assert response.status_code == 200
    assert len(response.json()['users']) == 1
