"""
CSV data loader.

Loads candidate and interviewer availability from CSV files.
"""

from typing import Dict, List
import csv
import logging
from .availability_loader import AvailabilityLoader

logger = logging.getLogger(__name__)


class CSVLoader(AvailabilityLoader):
    """Load availability data from CSV files."""
    
    def __init__(self, delimiter: str = ",", encoding: str = "utf-8"):
        """
        Initialize CSV loader.
        
        Args:
            delimiter: CSV delimiter character
            encoding: File encoding
        """
        super().__init__()
        self.delimiter = delimiter
        self.encoding = encoding
    
    def load(self, source: str) -> Dict:
        """
        Load from CSV file.
        
        Args:
            source: Path to CSV file
            
        Returns:
            Parsed data dictionary
        """
        raise NotImplementedError()
    
    def load_candidates(self, filepath: str) -> List[Dict]:
        """Load candidates from CSV."""
        raise NotImplementedError()
    
    def load_interviewers(self, filepath: str) -> List[Dict]:
        """Load interviewers from CSV."""
        raise NotImplementedError()
