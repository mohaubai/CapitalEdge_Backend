from fastapi.testclient import TestClient 
from main import app

client = TestClient(app)

def test_get_fraud_api_data():
    response = client.get('/fraud')
    assert response.status_code == 200