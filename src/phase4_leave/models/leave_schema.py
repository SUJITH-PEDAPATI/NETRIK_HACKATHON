"""Leave request and related data schemas."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LeaveRequest:
    """Leave request data model."""
    
    employee_id: str
    leave_type: str
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None
    approver_id: Optional[str] = None
    status: str = "PENDING"


@dataclass
class LeaveBalance:
    """Employee leave balance."""
    
    employee_id: str
    leave_type: str
    total_days: float
    used_days: float
    remaining_days: float


@dataclass
class LeavePolicy:
    """Company leave policy."""
    
    policy_id: str
    leave_type: str
    max_days_per_year: int
    carryover_allowed: bool
    advance_notice_days: int


@dataclass
class ApprovalLog:
    """Leave approval audit log."""
    
    request_id: str
    approver_id: str
    status: str
    timestamp: datetime
    comments: Optional[str] = None
