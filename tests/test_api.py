import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Book Recommendation API"}

def test_user_recommendations():
    response = client.get("/recommendations/user/1")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

def test_book_recommendations_structured():
    response = client.get("/recommendations/book/1?data_type=structured")
    assert response.status_code == 200
    data = response.json()
    assert "book_id" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

def test_book_recommendations_unstructured():
    response = client.get("/recommendations/book/1?data_type=unstructured")
    assert response.status_code == 200
    data = response.json()
    assert "book_id" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

def test_model_recommendations():
    response = client.get("/recommendations/model/1")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

def test_cluster_recommendations():
    response = client.get("/recommendations/cluster/1")
    assert response.status_code == 200
    data = response.json()
    assert "book_id" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
