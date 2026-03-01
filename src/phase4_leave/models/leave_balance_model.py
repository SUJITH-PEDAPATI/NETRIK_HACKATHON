# phase4_leave/models/leave_balance_model.py

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict
from .leave_type_enum import LeaveType


@dataclass
class LeaveBalance:
    """Employee leave balance tracking and calculation."""
    
    balance_id: str
    employee_id: str
    leave_type: LeaveType
    fiscal_year: int
    total_entitled_days: float
    used_days: float = 0.0
    approved_pending_days: float = 0.0
    pending_approval_days: float = 0.0
    carried_forward_days: float = 0.0
    adjusted_days: float = 0.0
    adjustment_reason: Optional[str] = None
    last_accrual_date: Optional[date] = None
    last_updated: datetime = field(default_factory=datetime.now)
    updated_by: Optional[str] = None
    
    @property
    def available_days(self) -> float:
        """Calculate available leave days."""
        return (
            self.total_entitled_days 
            + self.carried_forward_days 
            + self.adjusted_days 
            - self.used_days 
            - self.approved_pending_days
        )
    
    @property
    def remaining_days(self) -> float:
        """Remaining days available for new requests."""
        return self.available_days - self.pending_approval_days
    
    @property
    def utilization_percentage(self) -> float:
        """Calculate utilization percentage."""
        if self.total_entitled_days == 0:
            return 0.0
        return (self.used_days / self.total_entitled_days) * 100
    
    def can_approve_days(self, requested_days: float) -> bool:
        """Check if balance allows approval of requested days."""
        return requested_days <= self.available_days
    
    def can_accommodate_days(self, requested_days: float) -> bool:
        """Check if remaining balance can accommodate request."""
        return requested_days <= self.remaining_days


@dataclass
class LeaveAccrualHistory:
    """Track leave accrual over time."""
    
    accrual_id: str
    employee_id: str
    leave_type: LeaveType
    fiscal_year: int
    accrual_date: date
    accrued_days: float
    running_total: float
    accrual_reason: str
    accrued_by: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class EmployeeLeaveEntitlement:
    """Complete entitlement overview for an employee."""
    
    employee_id: str
    employee_name: str
    department_id: str
    designation: str
    tenure_days: int
    gender: Optional[str] = None
    balances: Dict[LeaveType, LeaveBalance] = field(default_factory=dict)
    last_sync: datetime = field(default_factory=datetime.now)
    
    def get_balance(self, leave_type: LeaveType) -> Optional[LeaveBalance]:
        """Get balance for specific leave type."""
        return self.balances.get(leave_type)
    
    def get_total_available(self) -> float:
        """Get total available days across all leave types."""
        return sum(balance.available_days for balance in self.balances.values())
    
    def get_total_utilization(self) -> float:
        """Get average utilization across all leave types."""
        if not self.balances:
            return 0.0
        total_utilization = sum(
            balance.utilization_percentage 
            for balance in self.balances.values()
        )
        return total_utilization / len(self.balances)
