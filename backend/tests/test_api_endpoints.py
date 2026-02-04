"""API endpoint tests for the RAG system.

Tests the FastAPI endpoints (/api/query, /api/courses) using mocked
dependencies to avoid external API calls and database dependencies.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock


def test_get_courses_endpoint(client: TestClient, mock_rag_system: Mock):
    """Test GET /api/courses returns course statistics."""
    # Act
    response = client.get("/api/courses")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "total_courses" in data
    assert "course_titles" in data
    assert data["total_courses"] == 2
    assert data["course_titles"] == ["Course A", "Course B"]

    # Verify mock was called
    mock_rag_system.get_course_analytics.assert_called_once()


def test_post_query_with_session_id(client: TestClient, mock_rag_system: Mock):
    """Test POST /api/query with provided session_id."""
    # Arrange
    query_data = {
        "query": "What is machine learning?",
        "session_id": "existing_session_123"
    }

    # Act
    response = client.post("/api/query", json=query_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "session_id" in data
    assert data["session_id"] == "existing_session_123"
    assert data["answer"] == "Test answer"
    assert data["sources"] == ["source1", "source2"]

    # Verify mock was called with correct arguments
    mock_rag_system.query.assert_called_once_with(
        "What is machine learning?", "existing_session_123"
    )
    # Session manager should NOT create a new session
    mock_rag_system.session_manager.create_session.assert_not_called()


def test_post_query_without_session_id(client: TestClient, mock_rag_system: Mock):
    """Test POST /api/query without session_id creates new session."""
    # Arrange
    query_data = {
        "query": "What is deep learning?"
    }
    mock_rag_system.session_manager.create_session.return_value = "new_session_456"

    # Act
    response = client.post("/api/query", json=query_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "new_session_456"

    # Verify mock was called with correct arguments
    mock_rag_system.query.assert_called_once_with(
        "What is deep learning?", "new_session_456"
    )
    mock_rag_system.session_manager.create_session.assert_called_once()


def test_post_query_error_handling(client: TestClient, mock_rag_system: Mock):
    """Test POST /api/query returns 500 when RAG system raises exception."""
    # Arrange
    query_data = {
        "query": "What is AI?",
        "session_id": "error_session"
    }
    mock_rag_system.query.side_effect = Exception("Something went wrong")

    # Act
    response = client.post("/api/query", json=query_data)

    # Assert
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Something went wrong" in data["detail"]


def test_get_courses_error_handling(client: TestClient, mock_rag_system: Mock):
    """Test GET /api/courses returns 500 when analytics fails."""
    # Arrange
    mock_rag_system.get_course_analytics.side_effect = Exception("Analytics error")

    # Act
    response = client.get("/api/courses")

    # Assert
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Analytics error" in data["detail"]


def test_query_request_validation(client: TestClient):
    """Test POST /api/query validation for missing query field."""
    # Arrange
    invalid_data = {"session_id": "some_session"}  # missing query

    # Act
    response = client.post("/api/query", json=invalid_data)

    # Assert
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    # Should have validation error about missing field


def test_cors_headers(client: TestClient):
    """Test CORS headers are present in responses."""
    # Act
    response = client.get("/api/courses", headers={"Origin": "http://localhost:3000"})

    # Assert
    assert response.headers.get("access-control-allow-origin") == "*"
    assert response.headers.get("access-control-allow-credentials") == "true"
    assert response.headers.get("access-control-expose-headers") == "*"


def test_root_endpoint(client: TestClient):
    """Test GET / returns health check message."""
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "RAG API is running" in data["message"]