"""
state_management/persistence/repository.py

Abstract repository interface for leave request storage.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class RepositoryInterface(ABC):
    """Abstract repository interface."""
    
    @abstractmethod
    def save(self, request_id: str, request_data: Dict) -> None:
        """Save a leave request."""
        pass
    
    @abstractmethod
    def load(self, request_id: str) -> Optional[Dict]:
        """Load a leave request."""
        pass
    
    @abstractmethod
    def update(self, request_id: str, request_data: Dict) -> None:
        """Update a leave request."""
        pass
    
    @abstractmethod
    def delete(self, request_id: str) -> None:
        """Delete a leave request."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Dict]:
        """List all leave requests."""
        pass
    
    @abstractmethod
    def find_by_state(self, state: str) -> List[Dict]:
        """Find requests by state."""
        pass
    
    @abstractmethod
    def find_by_employee(self, employee_id: str) -> List[Dict]:
        """Find requests by employee."""
        pass
