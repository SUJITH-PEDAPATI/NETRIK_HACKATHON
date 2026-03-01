"""
state_management/core/guards.py

Guard conditions for FSM transitions.
"""

from typing import Dict, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class GuardResult:
    """Result of guard evaluation."""
    allowed: bool
    reason: Optional[str] = None


class GuardConditions:
    """Guard conditions for leave transitions."""
    
    @staticmethod
    def has_balance(request: Dict, balance_info: Dict) -> GuardResult:
        """
        Guard: Employee has sufficient leave balance.
        
        Args:
            request: Leave request data
            balance_info: Employee leave balance
            
        Returns:
            GuardResult
        """
        leave_type = request.get("leave_type")
        balance = balance_info.get(leave_type, 0)
        
        start = datetime.strptime(request["start_date"], "%Y-%m-%d")
        end = datetime.strptime(request["end_date"], "%Y-%m-%d")
        days_requested = (end - start).days
        
        if balance < days_requested:
            return GuardResult(
                allowed=False,
                reason=f"Insufficient balance. Available: {balance}, Requested: {days_requested}"
            )
        
        return GuardResult(allowed=True)
    
    @staticmethod
    def no_overlapping_leaves(request: Dict, existing_leaves: list) -> GuardResult:
        """
        Guard: No overlapping approved leaves in same period.
        
        Args:
            request: Leave request data
            existing_leaves: List of existing approved leaves
            
        Returns:
            GuardResult
        """
        start = datetime.strptime(request["start_date"], "%Y-%m-%d")
        end = datetime.strptime(request["end_date"], "%Y-%m-%d")
        
        for leave in existing_leaves:
            if leave.get("state") in ["approved_hr", "completed"]:
                existing_start = datetime.strptime(leave["start_date"], "%Y-%m-%d")
                existing_end = datetime.strptime(leave["end_date"], "%Y-%m-%d")
                
                # Check overlap: start < existing_end AND end > existing_start
                if start < existing_end and end > existing_start:
                    return GuardResult(
                        allowed=False,
                        reason=f"Overlapping leave already approved"
                    )
        
        return GuardResult(allowed=True)
    
    @staticmethod
    def valid_leave_period(request: Dict) -> GuardResult:
        """
        Guard: Leave period is in future.
        
        Args:
            request: Leave request data
            
        Returns:
            GuardResult
        """
        today = datetime.now().date()
        start = datetime.strptime(request["start_date"], "%Y-%m-%d").date()
        
        if start < today:
            return GuardResult(
                allowed=False,
                reason="Cannot request leave in the past"
            )
        
        return GuardResult(allowed=True)
    
    @staticmethod
    def team_coverage(request: Dict, team_info: Dict) -> GuardResult:
        """
        Guard: Team has minimum coverage during leave.
        
        Args:
            request: Leave request data
            team_info: Team coverage information
            
        Returns:
            GuardResult
        """
        team_size = team_info.get("team_size", 1)
        approved_leaves_count = team_info.get("approved_leaves_during_period", 0)
        min_coverage = team_info.get("min_coverage", 1)
        
        if team_size - approved_leaves_count - 1 < min_coverage:
            return GuardResult(
                allowed=False,
                reason="Would breach minimum team coverage requirement"
            )
        
        return GuardResult(allowed=True)
    
    @staticmethod
    def manager_approval_required(request: Dict, role: str) -> GuardResult:
        """
        Guard: Transition requires manager approval.
        
        Args:
            request: Leave request data
            role: Current user role
            
        Returns:
            GuardResult
        """
        if role != "manager":
            return GuardResult(
                allowed=False,
                reason="Only manager can approve this transition"
            )
        
        return GuardResult(allowed=True)
    
    @staticmethod
    def hr_approval_required(request: Dict, role: str) -> GuardResult:
        """
        Guard: Transition requires HR approval.
        
        Args:
            request: Leave request data
            role: Current user role
            
        Returns:
            GuardResult
        """
        if role != "hr":
            return GuardResult(
                allowed=False,
                reason="Only HR can approve this transition"
            )
        
        return GuardResult(allowed=True)


class GuardRegistry:
    """Central registry for guard conditions."""
    
    def __init__(self):
        """Initialize guard registry."""
        self.guards: Dict[str, Callable] = {
            "has_balance": GuardConditions.has_balance,
            "no_overlap": GuardConditions.no_overlapping_leaves,
            "valid_period": GuardConditions.valid_leave_period,
            "coverage": GuardConditions.team_coverage,
            "manager": GuardConditions.manager_approval_required,
            "hr": GuardConditions.hr_approval_required,
        }
    
    def register_guard(self, name: str, guard_func: Callable) -> None:
        """Register custom guard condition."""
        self.guards[name] = guard_func
        logger.info(f"Registered guard: {name}")
    
    def evaluate_guard(self, guard_name: str, *args, **kwargs) -> GuardResult:
        """
        Evaluate a guard condition.
        
        Args:
            guard_name: Name of guard to evaluate
            args: Guard arguments
            kwargs: Guard keyword arguments
            
        Returns:
            GuardResult
        """
        guard = self.guards.get(guard_name)
        if not guard:
            return GuardResult(
                allowed=False,
                reason=f"Guard not found: {guard_name}"
            )
        
        try:
            return guard(*args, **kwargs)
        except Exception as e:
            logger.error(f"Guard evaluation failed: {e}")
            return GuardResult(
                allowed=False,
                reason=f"Guard evaluation error: {e}"
            )
