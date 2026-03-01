# phase4_leave/models/policy_utils.py

from .leave_type_enum import LeaveType
from .policy_registry import LEAVE_POLICIES
from .leave_policy_model import LeaveTypePolicy, LeavePolicy, LeaveEntitlement
from typing import List, Optional


def get_policy(leave_type: "LeaveType | str") -> LeaveTypePolicy:
    """Get base policy for a leave type."""
    if isinstance(leave_type, str):
        leave_type = LeaveType(leave_type)
    return LEAVE_POLICIES[leave_type]


def all_leave_types() -> List[LeaveType]:
    """Get all available leave types."""
    return list(LeaveType)


def get_applicable_entitlements(
    policy: LeavePolicy,
    tenure_months: int,
    designation: Optional[str] = None
) -> List[LeaveEntitlement]:
    """Get applicable entitlements based on tenure and designation."""
    results = []
    for entitlement in policy.entitlements:
        # Check tenure range
        if not (entitlement.min_tenure_months <= tenure_months):
            continue
        if entitlement.max_tenure_months and tenure_months > entitlement.max_tenure_months:
            continue
        
        # Check designation if specified
        if entitlement.designation and designation:
            if entitlement.designation != designation:
                continue
        
        if entitlement.is_active:
            results.append(entitlement)
    
    return results


def validate_leave_request(
    leave_type: LeaveType,
    duration_days: int,
    notice_days: int,
    employee_tenure_days: int,
    employee_balance: Optional[float] = None
) -> tuple[bool, List[str]]:
    """Validate leave request against policy constraints."""
    errors = []
    policy = get_policy(leave_type)
    
    # Check maximum days per request
    if duration_days > policy.max_days_per_request:
        errors.append(
            f"Request exceeds max {policy.max_days_per_request} days "
            f"for {leave_type.display()}"
        )
    
    # Check minimum notice
    if notice_days < policy.min_notice_days:
        errors.append(
            f"Minimum {policy.min_notice_days} days notice required "
            f"for {leave_type.display()}"
        )
    
    # Check minimum tenure
    if employee_tenure_days < policy.min_tenure_days:
        errors.append(
            f"Minimum {policy.min_tenure_days} days tenure required "
            f"for {leave_type.display()}"
        )
    
    # Check balance if provided
    if employee_balance is not None and employee_balance < duration_days:
        errors.append(
            f"Insufficient balance. Available: {employee_balance}, "
            f"Requested: {duration_days}"
        )
    
    return len(errors) == 0, errors


def calculate_accrual(
    leave_type: LeaveType,
    tenure_months: int,
    fiscal_months_worked: int
) -> float:
    """Calculate accrual for a given period."""
    policy = get_policy(leave_type)
    
    if policy.accrual_per_month == 0:
        return 0.0
    
    accrued = policy.accrual_per_month * fiscal_months_worked
    return round(accrued, 2)


def get_leave_policies_by_gender(gender: str) -> List[LeaveType]:
    """Get leave types applicable for a specific gender."""
    applicable = []
    for leave_type in all_leave_types():
        policy = get_policy(leave_type)
        if policy.eligible_genders is None or gender in policy.eligible_genders:
            applicable.append(leave_type)
    return applicable


def get_paid_leave_types() -> List[LeaveType]:
    """Get all paid leave types."""
    return [
        lt for lt in all_leave_types()
        if get_policy(lt).paid
    ]


def get_unpaid_leave_types() -> List[LeaveType]:
    """Get all unpaid leave types."""
    return [
        lt for lt in all_leave_types()
        if not get_policy(lt).paid
    ]