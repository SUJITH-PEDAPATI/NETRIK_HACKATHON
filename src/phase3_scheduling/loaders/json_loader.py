"""
JSON data loader.

Loads candidate and interviewer availability from JSON files.
"""

from typing import Dict, List
import json
import logging
from .availability_loader import AvailabilityLoader

logger = logging.getLogger(__name__)


class JSONLoader(AvailabilityLoader):
    """Load availability data from JSON files."""
    
    def __init__(self, validate_schema: bool = True):
        """
        Initialize JSON loader.
        
        Args:
            validate_schema: Whether to validate against schema
        """
        super().__init__()
        self.validate_schema = validate_schema
    
    def load(self, source: str) -> Dict:
        """
        Load from JSON file.
        
        Args:
            source: Path to JSON file
            
        Returns:
            Parsed data dictionary
        """
        raise NotImplementedError()
    
    def load_file(self, filepath: str) -> Dict:
        """Load and parse JSON file."""
        raise NotImplementedError()
    
    def validate(self, data: Dict) -> bool:
        """Validate against schema if enabled."""
        raise NotImplementedError()
