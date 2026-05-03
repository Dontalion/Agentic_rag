"""
PDF Analyzer Agent.
Specialized in reading and analyzing PDF documents.
"""
from smolagents import CodeAgent
from agentic_rag.config.config import get_settings
from agentic_rag.config.logging_config import get_logger
from agentic_rag.tools.pdf_analyzer_tool import PDFAnalyzerTool

logger = get_logger(__name__)
settings = get_settings()


def create_pdf_analyzer_agent(model) -> CodeAgent:
    """
    Create a PDF analyzer agent for document analysis.
    
    Args:
        model: The LLM model instance (InferenceClientModel).
    
    Returns:
        CodeAgent configured for PDF analysis tasks.
    """
    logger.info("Creating PDF analyzer agent")
    
    pdf_tool = PDFAnalyzerTool()
    pdf_analyzer_agent = CodeAgent(
        tools=[pdf_tool],
        model=model,
        name="pdf_analyzer_agent",
        description="Specialized in reading and analyzing PDF documents. Use this agent when you need to extract text, summarize content, or answer questions about a specific PDF file.",
    )
    
    return pdf_analyzer_agent
