"""
state_management/persistence/json_store.py

JSON file-based repository implementation.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json
import logging
from .repository import RepositoryInterface

logger = logging.getLogger(__name__)


class JSONStore(RepositoryInterface):
    """JSON file-based storage for leave requests."""
    
    def __init__(self, filepath: str):
        """
        Initialize JSON store.
        
        Args:
            filepath: Path to JSON file
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing data or create empty
        if self.filepath.exists():
            with open(self.filepath, 'r') as f:
                self.data: Dict[str, Dict] = json.load(f)
            logger.info(f"JSON store: Loaded {self.filepath}")
        else:
            self.data = {}
            logger.info(f"JSON store: Created new store at {self.filepath}")
    
    def _save_to_file(self) -> None:
        """Persist data to file."""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def save(self, request_id: str, request_data: Dict) -> None:
        """Save a leave request."""
        self.data[request_id] = request_data.copy()
        self._save_to_file()
        logger.info(f"JSON store: Saved {request_id}")
    
    def load(self, request_id: str) -> Optional[Dict]:
        """Load a leave request."""
        data = self.data.get(request_id)
        if data:
            logger.info(f"JSON store: Loaded {request_id}")
        return data.copy() if data else None
    
    def update(self, request_id: str, request_data: Dict) -> None:
        """Update a leave request."""
        if request_id in self.data:
            self.data[request_id].update(request_data)
            self._save_to_file()
            logger.info(f"JSON store: Updated {request_id}")
        else:
            logger.warning(f"JSON store: Request {request_id} not found")
    
    def delete(self, request_id: str) -> None:
        """Delete a leave request."""
        if request_id in self.data:
            del self.data[request_id]
            self._save_to_file()
            logger.info(f"JSON store: Deleted {request_id}")
        else:
            logger.warning(f"JSON store: Request {request_id} not found")
    
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
    
    def export(self, filepath: str) -> None:
        """
        Export data to another file.
        
        Args:
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        logger.info(f"JSON store: Exported to {filepath}")
    
    def get_stats(self) -> Dict:
        """Get storage statistics."""
        return {
            "filepath": str(self.filepath),
            "total_requests": len(self.data),
            "requests_by_state": {
                state: len([r for r in self.data.values() if r.get("state") == state])
                for state in set(r.get("state") for r in self.data.values())
            }
        }
