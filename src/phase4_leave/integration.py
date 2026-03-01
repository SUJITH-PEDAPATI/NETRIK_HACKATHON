"""
phase4_leave/integration.py

Integration module that ties together all components for the leave management system.
"""

import logging
from typing import Optional
from state_management.core import (
    LeaveStateMachine,
    GuardRegistry,
    TransitionRegistry,
)
from state_management.service import (
    StateService,
    HookRegistry,
    AuditLogger,
)
from state_management.persistence import (
    MemoryStore,
    JSONStore,
    SQLiteStore,
)
from state_management.cli import LeaveCLI

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class LeaveManagementSystem:
    """
    Integrated leave management system.
    
    Combines FSM, service layer, persistence, and CLI.
    """
    
    def __init__(self, storage_type: str = "memory", storage_path: Optional[str] = None):
        """
        Initialize the leave management system.
        
        Args:
            storage_type: "memory", "json", or "sqlite"
            storage_path: Path for file-based storage
        """
        # Initialize core FSM
        self.fsm = LeaveStateMachine()
        
        # Initialize registries
        self.guard_registry = GuardRegistry()
        self.transition_registry = TransitionRegistry()
        self.hook_registry = HookRegistry()
        
        # Initialize audit logger
        self.audit_logger = AuditLogger()
        
        # Initialize repository
        if storage_type == "memory":
            self.repository = MemoryStore()
            logger.info("Initialized with in-memory storage")
        elif storage_type == "json":
            if not storage_path:
                storage_path = "leave_requests.json"
            self.repository = JSONStore(storage_path)
            logger.info(f"Initialized with JSON storage: {storage_path}")
        elif storage_type == "sqlite":
            if not storage_path:
                storage_path = "leave_management.db"
            self.repository = SQLiteStore(storage_path)
            logger.info(f"Initialized with SQLite storage: {storage_path}")
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")
        
        # Initialize service
        self.service = StateService(
            fsm=self.fsm,
            guard_registry=self.guard_registry,
            transition_registry=self.transition_registry,
            hook_registry=self.hook_registry,
            audit_logger=self.audit_logger,
        )
        
        # Initialize CLI
        self.cli = LeaveCLI(
            state_service=self.service,
            repository=self.repository,
            audit_logger=self.audit_logger,
        )
        
        logger.info("Leave Management System initialized successfully")
    
    def create_request(self, request_data: dict) -> str:
        """Create a new leave request."""
        request_id = self.service.create_request(request_data)
        
        # Save to repository
        request = self.service.get_request(request_id)
        self.repository.save(request_id, request)
        
        return request_id
    
    def submit_request(self, request_id: str, employee_id: str) -> tuple[bool, str]:
        """Submit a leave request."""
        success, error = self.service.transition(
            request_id,
            "submitted",
            employee_id,
            "employee",
        )
        
        if success:
            request = self.service.get_request(request_id)
            self.repository.update(request_id, request)
        
        return success, error
    
    def approve_by_manager(
        self,
        request_id: str,
        manager_id: str,
    ) -> tuple[bool, str]:
        """Manager approves a leave request."""
        success, error = self.service.transition(
            request_id,
            "approved_manager",
            manager_id,
            "manager",
        )
        
        if success:
            request = self.service.get_request(request_id)
            self.repository.update(request_id, request)
        
        return success, error
    
    def approve_by_hr(self, request_id: str, hr_id: str) -> tuple[bool, str]:
        """HR approves a leave request."""
        success, error = self.service.transition(
            request_id,
            "approved_hr",
            hr_id,
            "hr",
        )
        
        if success:
            request = self.service.get_request(request_id)
            self.repository.update(request_id, request)
        
        return success, error
    
    def reject_request(
        self,
        request_id: str,
        user_id: str,
        user_role: str,
        reason: str,
    ) -> tuple[bool, str]:
        """Reject a leave request."""
        success, error = self.service.transition(
            request_id,
            "rejected",
            user_id,
            user_role,
            reason=reason,
        )
        
        if success:
            request = self.service.get_request(request_id)
            self.repository.update(request_id, request)
        
        return success, error
    
    def cancel_request(
        self,
        request_id: str,
        user_id: str,
        reason: str = None,
    ) -> tuple[bool, str]:
        """Cancel a leave request."""
        success, error = self.service.transition(
            request_id,
            "cancelled",
            user_id,
            "employee",
            reason=reason,
        )
        
        if success:
            request = self.service.get_request(request_id)
            self.repository.update(request_id, request)
        
        return success, error
    
    def get_request_status(self, request_id: str) -> dict:
        """Get current request status."""
        return self.service.get_request(request_id)
    
    def get_request_history(self, request_id: str) -> list:
        """Get request audit history."""
        return self.audit_logger.get_request_history(request_id)
    
    def get_system_stats(self) -> dict:
        """Get system statistics."""
        return {
            "audit": self.audit_logger.get_stats(),
            "storage": self.repository.get_stats() if hasattr(self.repository, 'get_stats') else {},
        }


# Example usage
if __name__ == "__main__":
    # Initialize system with in-memory storage
    system = LeaveManagementSystem(storage_type="memory")
    
    # Create a leave request
    request_data = {
        "request_id": "REQ-001",
        "employee_id": "EMP-001",
        "leave_type": "paid",
        "start_date": "2024-12-25",
        "end_date": "2024-12-26",
        "reason": "Holiday vacation",
    }
    
    request_id = system.create_request(request_data)
    print(f"Created request: {request_id}")
    
    # Submit request
    success, error = system.submit_request(request_id, "EMP-001")
    print(f"Submit: {success} - {error if error else 'Success'}")
    
    # Manager approves
    success, error = system.approve_by_manager(request_id, "MGR-001")
    print(f"Manager approval: {success} - {error if error else 'Success'}")
    
    # Get status
    status = system.get_request_status(request_id)
    print(f"Current status: {status.get('state')}")
    
    # Get stats
    stats = system.get_system_stats()
    print(f"System stats: {stats}")
