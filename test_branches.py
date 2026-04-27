from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_branches():
    response = client.get("/branches")
    assert response.status_code == 200

def test_get_branches_by_id():
    response = client.get("/branches/1")
    assert response.status_code == 200
    assert response.json()['data']['branch_id'] == 1