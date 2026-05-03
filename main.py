"""
Agentic RAG - Main Entry Point

This script initializes and runs the multi-agent RAG system.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.multi_agent_system import main

if __name__ == "__main__":
    main()
