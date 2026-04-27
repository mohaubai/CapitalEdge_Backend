from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analytics_endpoint():
    response = client.get("/analytics")
    assert response.status_code == 200
    assert isinstance(response.json()[0]['year'], int)