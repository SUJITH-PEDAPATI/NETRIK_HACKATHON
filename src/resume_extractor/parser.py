import logging
from pathlib import Path
from typing import Dict, List, Optional
from .pdf_extractor import PDFExtractor
from .ocr_engine import OCREngine
from .docs_extractor import DocsExtractor

logger = logging.getLogger(__name__)

class ResumeParser:
    """Orchestrates resume parsing pipeline: extraction  structured data"""

    def __init__(self, use_ocr: bool = False, ocr_path: Optional[str] = None):
        """Initialize parser with extractors"""
        self.pdf_extractor = PDFExtractor()
        self.ocr_engine = OCREngine(tesseract_path=ocr_path) if use_ocr else None
        self.docs_extractor = DocsExtractor()

    def parse_file(self, file_path: str) -> Dict:
        """Parse a single resume file"""
        file_path = Path(file_path)
        
        # Step 1: Extract raw text
        if file_path.suffix.lower() == ".pdf":
            resume_text = self.pdf_extractor.extract_from_pdf(str(file_path))
        elif file_path.suffix.lower() == ".docx":
            resume_text = self.pdf_extractor.extract_from_docx(str(file_path))
        else:
            logger.warning(f"Unsupported file format: {file_path.suffix}")
            return {}
        
        if not resume_text:
            logger.warning(f"No text extracted from {file_path}")
            return {}
        
        # Step 2: Extract structured data
        structured_data = self.docs_extractor.extract(resume_text)
        structured_data["raw_text"] = resume_text
        structured_data["file_path"] = str(file_path)
        
        return structured_data

    def parse_folder(self, folder_path: str) -> List[Dict]:
        """Parse all resume files in a folder"""
        folder_path = Path(folder_path)
        results = []
        
        supported_formats = (".pdf", ".docx", ".doc")
        
        for file_path in folder_path.iterdir():
            if file_path.suffix.lower() in supported_formats:
                logger.info(f"Parsing {file_path.name}...")
                try:
                    parsed = self.parse_file(str(file_path))
                    if parsed:
                        results.append(parsed)
                except Exception as e:
                    logger.error(f"Error parsing {file_path.name}: {e}")
        
        logger.info(f"Successfully parsed {len(results)} resume(s)")
        return results
