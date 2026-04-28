from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_customer_endpoint():
    response = client.get('/customers/1/summary')
    assert response.status_code == 200
    assert isinstance(response.json()[0]['name'], str)
    assert isinstance(response.json()[0]['city'], str)
    assert isinstance(response.json()[0]['account_count'], int)