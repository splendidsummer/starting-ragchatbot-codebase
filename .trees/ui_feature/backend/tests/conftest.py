import pytest
import sys
import os
from unittest.mock import Mock, AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Dict, Any, List

# Add parent directory to sys.path to allow importing backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import Config
from rag_system import RAGSystem
from vector_store import VectorStore
from ai_generator import AIGenerator
from session_manager import SessionManager


@pytest.fixture
def mock_config() -> Config:
    """Mock configuration for testing."""
    config = Config(
        ANTHROPIC_API_KEY="test_api_key",
        ANTHROPIC_BASE_URL="http://test.example.com",
        ANTHROPIC_MODEL="test-model",
        EMBEDDING_MODEL="test-embedding-model",
        CHUNK_SIZE=800,
        CHUNK_OVERLAP=100,
        MAX_RESULTS=5,
        MAX_HISTORY=2,
        CHROMA_PATH="./test_chroma_db"
    )
    return config


@pytest.fixture
def mock_vector_store() -> Mock:
    """Mock VectorStore with minimal methods."""
    mock = Mock(spec=VectorStore)
    mock.search.return_value = [
        {
            "text": "Sample course content about machine learning.",
            "course_title": "Machine Learning 101",
            "lesson_title": "Introduction to ML",
            "metadata": {"course": "Machine Learning 101", "lesson": "Lesson 1"}
        }
    ]
    mock.get_course_analytics.return_value = {
        "total_courses": 2,
        "course_titles": ["Machine Learning 101", "Data Science Fundamentals"]
    }
    mock.get_existing_course_titles.return_value = ["Machine Learning 101", "Data Science Fundamentals"]
    mock.add_course_metadata = Mock()
    mock.add_course_content = Mock()
    mock.clear_all_data = Mock()
    return mock


@pytest.fixture
def mock_ai_generator() -> Mock:
    """Mock AIGenerator with query method."""
    mock = Mock(spec=AIGenerator)
    mock.query.return_value = (
        "This is a generated answer based on the search results.",
        ["source1", "source2"]
    )
    return mock


@pytest.fixture
def mock_session_manager() -> Mock:
    """Mock SessionManager."""
    mock = Mock(spec=SessionManager)
    mock.create_session.return_value = "test_session_id"
    mock.get_session_history.return_value = []
    mock.add_to_session = Mock()
    return mock


@pytest.fixture
def mock_rag_system(
    mock_config: Config,
    mock_vector_store: Mock,
    mock_ai_generator: Mock,
    mock_session_manager: Mock
) -> Mock:
    """Mock RAGSystem with all dependencies mocked."""
    mock = Mock(spec=RAGSystem)
    mock.config = mock_config
    mock.vector_store = mock_vector_store
    mock.ai_generator = mock_ai_generator
    mock.session_manager = mock_session_manager
    mock.query = Mock(return_value=("Test answer", ["source1", "source2"]))
    mock.get_course_analytics = Mock(return_value={
        "total_courses": 2,
        "course_titles": ["Course A", "Course B"]
    })
    return mock


@pytest.fixture
def test_app(mock_rag_system: Mock) -> FastAPI:
    """Create a FastAPI test app without static file mounts.

    This app replicates the API endpoints from backend/app.py but without
    mounting static files that don't exist in test environment.
    """
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    from pydantic import BaseModel
    from typing import List, Optional

    # Create app without static mounts
    app = FastAPI(title="Course Materials RAG System - Test", root_path="")

    # Add trusted host middleware for proxy
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]
    )

    # Enable CORS with proper settings for proxy
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Pydantic models for request/response (duplicated from app.py)
    class QueryRequest(BaseModel):
        """Request model for course queries"""
        query: str
        session_id: Optional[str] = None

    class QueryResponse(BaseModel):
        """Response model for course queries"""
        answer: str
        sources: List[str]
        session_id: str

    class CourseStats(BaseModel):
        """Response model for course statistics"""
        total_courses: int
        course_titles: List[str]

    # API Endpoints
    @app.post("/api/query", response_model=QueryResponse)
    async def query_documents(request: QueryRequest):
        """Process a query and return response with sources"""
        try:
            # Create session if not provided
            session_id = request.session_id
            if not session_id:
                session_id = mock_rag_system.session_manager.create_session()

            # Process query using RAG system
            answer, sources = mock_rag_system.query(request.query, session_id)

            return QueryResponse(
                answer=answer,
                sources=sources,
                session_id=session_id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/courses", response_model=CourseStats)
    async def get_course_stats():
        """Get course analytics and statistics"""
        try:
            analytics = mock_rag_system.get_course_analytics()
            return CourseStats(
                total_courses=analytics["total_courses"],
                course_titles=analytics["course_titles"]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Root endpoint for health check (replaces static file mount)
    @app.get("/")
    async def root():
        return {"status": "ok", "message": "RAG API is running"}

    return app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    """Test client for the FastAPI app."""
    return TestClient(test_app)


@pytest.fixture
def sample_query_request() -> Dict[str, Any]:
    """Sample query request data."""
    return {
        "query": "What is machine learning?",
        "session_id": "test_session_123"
    }


@pytest.fixture
def sample_course_stats() -> Dict[str, Any]:
    """Sample course statistics data."""
    return {
        "total_courses": 2,
        "course_titles": ["Machine Learning 101", "Data Science Fundamentals"]
    }