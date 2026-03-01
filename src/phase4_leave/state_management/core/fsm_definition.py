"""
state_management/core/fsm_definition.py

Finite State Machine definition for leave management.
Pure logic layer - no side effects.
"""

from enum import Enum
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class LeaveState(Enum):
    """Leave request states."""
    DRAFT = "draft"                    # Initial creation
    SUBMITTED = "submitted"            # Awaiting approval
    APPROVED_MANAGER = "approved_mgr"  # Manager approved
    APPROVED_HR = "approved_hr"        # HR approved (final)
    REJECTED = "rejected"              # Rejected at any stage
    CANCELLED = "cancelled"            # Cancelled by employee
    COMPLETED = "completed"            # Leave period ended
    FAILED = "failed"                  # System error


class LeaveType(Enum):
    """Types of leave."""
    PAID = "paid"
    UNPAID = "unpaid"
    SICK = "sick"
    PERSONAL = "personal"
    BEREAVEMENT = "bereavement"
    MATERNITY = "maternity"
    SABBATICAL = "sabbatical"


@dataclass
class LeaveRequest:
    """Leave request object."""
    request_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: str
    end_date: str
    reason: str
    state: LeaveState = LeaveState.DRAFT
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class LeaveStateMachine:
    """
    Pure FSM definition for leave management.
    Defines valid transitions and state rules.
    """
    
    def __init__(self):
        """Initialize FSM with state definitions."""
        # Valid transitions: from_state -> {to_states}
        self.transitions: Dict[LeaveState, Set[LeaveState]] = {
            LeaveState.DRAFT: {
                LeaveState.SUBMITTED,
                LeaveState.CANCELLED,
            },
            LeaveState.SUBMITTED: {
                LeaveState.APPROVED_MANAGER,
                LeaveState.REJECTED,
                LeaveState.CANCELLED,
            },
            LeaveState.APPROVED_MANAGER: {
                LeaveState.APPROVED_HR,
                LeaveState.REJECTED,
                LeaveState.CANCELLED,
            },
            LeaveState.APPROVED_HR: {
                LeaveState.COMPLETED,
                LeaveState.CANCELLED,
            },
            LeaveState.REJECTED: set(),      # Terminal state
            LeaveState.CANCELLED: set(),     # Terminal state
            LeaveState.COMPLETED: set(),     # Terminal state
            LeaveState.FAILED: {
                LeaveState.DRAFT,             # Recovery: back to draft
            },
        }
        
        # State requirements/metadata
        self.state_requirements = {
            LeaveState.DRAFT: {
                "approval_count": 0,
                "is_terminal": False,
            },
            LeaveState.SUBMITTED: {
                "approval_count": 0,
                "is_terminal": False,
                "requires_manager": True,
            },
            LeaveState.APPROVED_MANAGER: {
                "approval_count": 1,
                "is_terminal": False,
                "requires_hr": True,
            },
            LeaveState.APPROVED_HR: {
                "approval_count": 2,
                "is_terminal": False,
                "ready_for_execution": True,
            },
            LeaveState.REJECTED: {
                "is_terminal": True,
            },
            LeaveState.CANCELLED: {
                "is_terminal": True,
            },
            LeaveState.COMPLETED: {
                "is_terminal": True,
            },
            LeaveState.FAILED: {
                "is_terminal": False,
                "error_state": True,
            },
        }
    
    def get_valid_transitions(self, state: LeaveState) -> Set[LeaveState]:
        """
        Get all valid target states from current state.
        
        Args:
            state: Current state
            
        Returns:
            Set of valid next states
        """
        return self.transitions.get(state, set())
    
    def is_valid_transition(
        self,
        from_state: LeaveState,
        to_state: LeaveState,
    ) -> bool:
        """
        Check if transition is valid.
        
        Args:
            from_state: Current state
            to_state: Target state
            
        Returns:
            True if transition is allowed
        """
        valid_targets = self.transitions.get(from_state, set())
        return to_state in valid_targets
    
    def is_terminal_state(self, state: LeaveState) -> bool:
        """
        Check if state is terminal (no further transitions).
        
        Args:
            state: State to check
            
        Returns:
            True if terminal
        """
        return self.state_requirements.get(state, {}).get("is_terminal", False)
    
    def get_all_transitions(self) -> Dict[LeaveState, List[LeaveState]]:
        """
        Get all transitions for documentation.
        
        Returns:
            Dictionary of all valid transitions
        """
        return {
            from_state: list(to_states)
            for from_state, to_states in self.transitions.items()
        }
    
    def get_state_info(self, state: LeaveState) -> Dict:
        """
        Get information about a specific state.
        
        Args:
            state: State to query
            
        Returns:
            State metadata
        """
        return self.state_requirements.get(state, {})


class LeaveRequestValidator:
    """Validates leave request data."""
    
    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> tuple[bool, Optional[str]]:
        """Validate date range."""
        try:
            from datetime import datetime
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start > end:
                return False, "Start date must be before end date"
            
            if start == end:
                return False, "Leave must be at least 1 day"
            
            return True, None
        except ValueError as e:
            return False, f"Invalid date format: {e}"
    
    @staticmethod
    def validate_request(request: LeaveRequest) -> tuple[bool, Optional[str]]:
        """
        Validate complete leave request.
        
        Args:
            request: Leave request to validate
            
        Returns:
            (is_valid, error_message)
        """
        # Check required fields
        if not request.employee_id:
            return False, "Employee ID is required"
        
        if not request.reason:
            return False, "Reason is required"
        
        # Validate dates
        is_valid, error = LeaveRequestValidator.validate_dates(
            request.start_date,
            request.end_date
        )
        if not is_valid:
            return False, error
        
        return True, None
