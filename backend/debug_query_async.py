
import sys
import os
import asyncio
# Add current directory to path so imports work
sys.path.append(os.getcwd())

from config import config
from rag_system import RAGSystem
import traceback

async def test():
    print(f"Anthropic API Key present: {bool(config.ANTHROPIC_API_KEY)}")
    print(f"Base URL: {config.ANTHROPIC_BASE_URL}")
    print(f"Model: {config.ANTHROPIC_MODEL}")
    
    try:
        rag = RAGSystem(config)
        print("RAG System initialized")
        
        # Create session
        session_id = rag.session_manager.create_session()
        print(f"Session created: {session_id}")
        
        # Try query
        print("Attempting query...")
        answer, sources = rag.query("What is in the course?", session_id)
        print(f"Answer: {answer}")
        
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
