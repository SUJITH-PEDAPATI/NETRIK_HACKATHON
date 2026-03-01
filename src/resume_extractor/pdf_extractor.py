import pdfplumber
from docx import Document
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extract text from PDF and DOCX files using pdfplumber and python-docx"""

    @staticmethod
    def extract_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting PDF {pdf_path}: {e}")
            return ""

    @staticmethod
    def extract_from_docx(docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(docx_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting DOCX {docx_path}: {e}")
            return ""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        file_path = Path(file_path)
        if file_path.suffix.lower() == ".pdf":
            return PDFExtractor.extract_from_pdf(str(file_path))
        elif file_path.suffix.lower() == ".docx":
            return PDFExtractor.extract_from_docx(str(file_path))
        else:
            logger.warning(f"Unsupported file format: {file_path.suffix}")
            return ""