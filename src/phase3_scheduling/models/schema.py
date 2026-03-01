"""
Data schemas for validation.

Defines validation schemas for input/output data structures.
"""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Base schema validator."""
    
    def validate(self, data: Dict) -> bool:
        """Validate data against schema."""
        raise NotImplementedError()
    
    def get_errors(self, data: Dict) -> List[str]:
        """Get validation error messages."""
        raise NotImplementedError()


class ScheduleSchema(SchemaValidator):
    """Validation schema for schedules."""
    
    def __init__(self):
        """Initialize schedule schema."""
        logger.info("Initialized ScheduleSchema")
    
    def validate(self, schedule: Dict) -> bool:
        """Validate schedule structure."""
        raise NotImplementedError()


class CandidateSchema(SchemaValidator):
    """Validation schema for candidate data."""
    
    def __init__(self):
        """Initialize candidate schema."""
        logger.info("Initialized CandidateSchema")
    
    def validate(self, candidate: Dict) -> bool:
        """Validate candidate data structure."""
        raise NotImplementedError()


class InterviewerSchema(SchemaValidator):
    """Validation schema for interviewer data."""
    
    def __init__(self):
        """Initialize interviewer schema."""
        logger.info("Initialized InterviewerSchema")
    
    def validate(self, interviewer: Dict) -> bool:
        """Validate interviewer data structure."""
        raise NotImplementedError()
