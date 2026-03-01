"""
state_management/persistence/memory_store.py

In-memory repository implementation for development/testing.
"""

from typing import Dict, List, Optional
import logging
from .repository import RepositoryInterface

logger = logging.getLogger(__name__)


class MemoryStore(RepositoryInterface):
    """In-memory storage for leave requests."""
    
    def __init__(self):
        """Initialize memory store."""
        self.data: Dict[str, Dict] = {}
    
    def save(self, request_id: str, request_data: Dict) -> None:
        """Save a leave request."""
        self.data[request_id] = request_data.copy()
        logger.info(f"Memory store: Saved {request_id}")
    
    def load(self, request_id: str) -> Optional[Dict]:
        """Load a leave request."""
        data = self.data.get(request_id)
        if data:
            logger.info(f"Memory store: Loaded {request_id}")
        return data.copy() if data else None
    
    def update(self, request_id: str, request_data: Dict) -> None:
        """Update a leave request."""
        if request_id in self.data:
            self.data[request_id].update(request_data)
            logger.info(f"Memory store: Updated {request_id}")
        else:
            logger.warning(f"Memory store: Request {request_id} not found")
    
    def delete(self, request_id: str) -> None:
        """Delete a leave request."""
        if request_id in self.data:
            del self.data[request_id]
            logger.info(f"Memory store: Deleted {request_id}")
        else:
            logger.warning(f"Memory store: Request {request_id} not found")
    
    def list_all(self) -> List[Dict]:
        """List all leave requests."""
        return [req.copy() for req in self.data.values()]
    
    def find_by_state(self, state: str) -> List[Dict]:
        """Find requests by state."""
        return [
            req.copy() for req in self.data.values()
            if req.get("state") == state
        ]
    
    def find_by_employee(self, employee_id: str) -> List[Dict]:
        """Find requests by employee."""
        return [
            req.copy() for req in self.data.values()
            if req.get("employee_id") == employee_id
        ]
    
    def clear(self) -> None:
        """Clear all data (for testing)."""
        self.data.clear()
        logger.info("Memory store: Cleared")
    
    def get_stats(self) -> Dict:
        """Get storage statistics."""
        return {
            "total_requests": len(self.data),
            "requests_by_state": {
                state: len([r for r in self.data.values() if r.get("state") == state])
                for state in set(r.get("state") for r in self.data.values())
            }
        }
