"""
state_management/persistence/sqlite_store.py

SQLite database repository implementation.
"""

from typing import Dict, List, Optional
from pathlib import Path
import sqlite3
import json
import logging
from .repository import RepositoryInterface

logger = logging.getLogger(__name__)


class SQLiteStore(RepositoryInterface):
    """SQLite database storage for leave requests."""
    
    def __init__(self, filepath: str):
        """
        Initialize SQLite store.
        
        Args:
            filepath: Path to SQLite database file
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.connection_string = str(self.filepath)
        
        self._init_db()
        logger.info(f"SQLite store: Initialized at {self.filepath}")
    
    def _get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.connection_string)
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_requests (
                request_id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL,
                state TEXT NOT NULL,
                leave_type TEXT,
                start_date TEXT,
                end_date TEXT,
                reason TEXT,
                created_at TEXT,
                updated_at TEXT,
                created_by TEXT,
                updated_by TEXT,
                metadata TEXT,
                data TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_employee 
            ON leave_requests(employee_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_state 
            ON leave_requests(state)
        """)
        
        conn.commit()
        conn.close()
    
    def save(self, request_id: str, request_data: Dict) -> None:
        """Save a leave request."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO leave_requests 
            (request_id, employee_id, state, data)
            VALUES (?, ?, ?, ?)
        """, (
            request_id,
            request_data.get("employee_id"),
            request_data.get("state"),
            json.dumps(request_data)
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"SQLite store: Saved {request_id}")
    
    def load(self, request_id: str) -> Optional[Dict]:
        """Load a leave request."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT data FROM leave_requests WHERE request_id = ?",
            (request_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            logger.info(f"SQLite store: Loaded {request_id}")
            return json.loads(row[0])
        
        return None
    
    def update(self, request_id: str, request_data: Dict) -> None:
        """Update a leave request."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get existing data
        cursor.execute(
            "SELECT data FROM leave_requests WHERE request_id = ?",
            (request_id,)
        )
        row = cursor.fetchone()
        
        if row:
            existing = json.loads(row[0])
            existing.update(request_data)
            
            cursor.execute("""
                UPDATE leave_requests 
                SET state = ?, data = ?
                WHERE request_id = ?
            """, (
                existing.get("state"),
                json.dumps(existing),
                request_id
            ))
            
            conn.commit()
            logger.info(f"SQLite store: Updated {request_id}")
        else:
            logger.warning(f"SQLite store: Request {request_id} not found")
        
        conn.close()
    
    def delete(self, request_id: str) -> None:
        """Delete a leave request."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM leave_requests WHERE request_id = ?", (request_id,))
        conn.commit()
        conn.close()
        logger.info(f"SQLite store: Deleted {request_id}")
    
    def list_all(self) -> List[Dict]:
        """List all leave requests."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM leave_requests")
        rows = cursor.fetchall()
        conn.close()
        
        return [json.loads(row[0]) for row in rows]
    
    def find_by_state(self, state: str) -> List[Dict]:
        """Find requests by state."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT data FROM leave_requests WHERE state = ?",
            (state,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [json.loads(row[0]) for row in rows]
    
    def find_by_employee(self, employee_id: str) -> List[Dict]:
        """Find requests by employee."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT data FROM leave_requests WHERE employee_id = ?",
            (employee_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [json.loads(row[0]) for row in rows]
    
    def get_stats(self) -> Dict:
        """Get storage statistics."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM leave_requests")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT state, COUNT(*) FROM leave_requests GROUP BY state
        """)
        stats_by_state = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            "filepath": self.filepath,
            "total_requests": total,
            "requests_by_state": stats_by_state
        }
