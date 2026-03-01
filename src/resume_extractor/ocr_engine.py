import cv2
import pytesseract
from PIL import Image
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OCREngine:
    """OCR extraction for scanned PDFs using Tesseract"""

    def __init__(self, tesseract_path: Optional[str] = None):
        """Initialize OCR engine. Set tesseract_path if not in system PATH"""
        if tesseract_path:
            pytesseract.pytesseract.pytesseract_cmd = tesseract_path

    @staticmethod
    def extract_from_image(image_path: str) -> str:
        """Extract text from image using Tesseract OCR"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"Could not read image: {image_path}")
                return ""
            
            # Preprocess for better OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from image {image_path}: {e}")
            return ""

    @staticmethod
    def extract_from_pdf_page(pdf_page_image) -> str:
        """Extract text from a PDF page image using Tesseract"""
        try:
            text = pytesseract.image_to_string(pdf_page_image)
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF page: {e}")
            return ""