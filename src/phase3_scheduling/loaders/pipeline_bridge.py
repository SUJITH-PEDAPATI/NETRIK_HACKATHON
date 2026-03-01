"""
Bridge module connecting resume pipeline to scheduling pipeline.

Transforms candidate data from Phase 1-2 into scheduling format.
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PipelineBridge:
    """Bridges resume/interview pipelines with scheduling pipeline."""
    
    def __init__(self):
        """Initialize pipeline bridge."""
        logger.info("Initialized PipelineBridge")
    
    def transform_candidate_data(self, candidate: Dict) -> Dict:
        """
        Transform candidate from previous phases into scheduling format.
        
        Args:
            candidate: Candidate data from resume or interview phase
            
        Returns:
            Candidate data in scheduling format
        """
        raise NotImplementedError()
    
    def transform_interviewer_data(self, interviewer: Dict) -> Dict:
        """Transform interviewer data to scheduling format."""
        raise NotImplementedError()
    
    def reverse_transform_schedule(self, schedule: Dict) -> Dict:
        """Convert schedule back to pipeline format for downstream phases."""
        raise NotImplementedError()
