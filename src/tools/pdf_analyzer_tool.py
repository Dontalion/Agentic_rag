"""
PDF Analyzer Tool for smolagents.
Reads and extracts text from PDF files, then provides analysis.
"""
from smolagents import Tool
from pypdf import PdfReader
import os


class PDFAnalyzerTool(Tool):
    name = "pdf_analyzer"
    description = """
    Analyzes a PDF file and extracts its text content.
    Use this tool when you need to read, summarize, or answer questions about a PDF document.
    The tool returns the full text content of the PDF along with metadata.
    """
    inputs = {
        "pdf_path": {
            "type": "string",
            "description": "The file path to the PDF file to analyze. Must be an absolute or relative path to a valid .pdf file.",
        },
        "max_pages": {
            "type": "integer",
            "description": "Maximum number of pages to extract. Use -1 for all pages. Default is 10.",
        },
    }
    output_type = "string"

    def forward(self, pdf_path: str, max_pages: int = 10) -> str:
        if not os.path.exists(pdf_path):
            return f"Error: File not found at path '{pdf_path}'. Please provide a valid PDF file path."

        if not pdf_path.lower().endswith(".pdf"):
            return f"Error: '{pdf_path}' does not appear to be a PDF file. Please provide a file with a .pdf extension."

        try:
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)

            metadata = reader.metadata
            metadata_str = ""
            if metadata:
                metadata_str = "PDF Metadata:\n"
                for key, value in metadata.items():
                    metadata_str += f"  {key}: {value}\n"
                metadata_str += "\n"

            pages_to_read = min(max_pages, num_pages) if max_pages != -1 else num_pages

            text_content = []
            for i in range(pages_to_read):
                page = reader.pages[i]
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"--- Page {i + 1} ---\n{page_text}")

            extracted_text = "\n\n".join(text_content)

            result = f"""{metadata_str}PDF Analysis Results:
- File: {pdf_path}
- Total pages: {num_pages}
- Pages extracted: {pages_to_read}

{'='*80}
EXTRACTED TEXT:
{'='*80}

{extracted_text}

{'='*80}
End of PDF content.
"""
            return result

        except Exception as e:
            return f"Error analyzing PDF '{pdf_path}': {type(e).__name__}: {str(e)}"
