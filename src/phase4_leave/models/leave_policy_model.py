# phase4_leave/models/leave_policy_model.py

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable
from datetime import date
from .leave_type_enum import LeaveType


@dataclass(frozen=True)
class LeaveTypePolicy:
    """Core leave policy configuration."""
    
    leave_type:            LeaveType
    max_days_per_request:  int
    max_days_per_year:     int
    min_notice_days:       int
    requires_document:     bool
    carries_forward:       bool
    paid:                  bool
    eligible_genders:      Optional[list[str]] = None
    min_tenure_days:       int = 0
    cooldown_days:         int = 0
    can_overlap_team:      bool = False
    max_team_overlap_pct:  float = 0.0
    accrual_per_month:     float = 0.0
    description:           str = ""
    max_carryforward_days: float = 0.0
    carryforward_expiry_months: int = 12
    fractional_days_allowed: bool = True
    requires_approval:     bool = True
    auto_approve_threshold_days: float = 5.0
    block_leaves_before_notice: bool = True
    employee_cap_per_month: Optional[int] = None
    department_cap_percentage: Optional[float] = None
    restricted_dates: List[date] = field(default_factory=list)
    restricted_periods: List[tuple[date, date]] = field(default_factory=list)


@dataclass
class LeaveEntitlement:
    """Defines leave entitlement rules based on tenure and designation."""
    
    entitlement_id: str
    leave_type: LeaveType
    designation: Optional[str]
    min_tenure_months: int
    max_tenure_months: Optional[int]
    entitled_days_per_year: float
    accrual_frequency: str  # 'monthly', 'quarterly', 'yearly'
    is_active: bool = True


@dataclass
class LeavePolicy:
    """Advanced leave policy with multiple entitlements."""
    
    policy_id: str
    policy_name: str
    effective_from: date
    effective_to: Optional[date] = None
    leave_type: LeaveType = LeaveType.ANNUAL
    base_policy: LeaveTypePolicy = None
    entitlements: List[LeaveEntitlement] = field(default_factory=list)
    exceptions: Dict[str, str] = field(default_factory=dict)
    version: int = 1
    is_active: bool = True
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    
    def get_entitlements_for_tenure(self, tenure_months: int) -> List[LeaveEntitlement]:
        """Get applicable entitlements for given tenure."""
        return [
            e for e in self.entitlements
            if e.min_tenure_months <= tenure_months 
            and (e.max_tenure_months is None or tenure_months <= e.max_tenure_months)
        ]


@dataclass
class PolicyConstraint:
    """Define constraints and rules for leave policies."""
    
    constraint_id: str
    policy_id: str
    constraint_type: str  # 'overlap', 'consecutive_days', 'department', 'timing'
    rule_description: str
    is_hard_constraint: bool = True
    applies_to_leave_types: List[LeaveType] = field(default_factory=list)
    condition: Optional[Callable] = None
    penalty_or_action: Optional[str] = None
