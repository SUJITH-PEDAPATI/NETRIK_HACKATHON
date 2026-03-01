"""
state_management/core/transitions.py

Transition definitions and metadata.
"""

from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class TransitionInfo:
    """Information about a transition."""
    from_state: str
    to_state: str
    name: str
    description: str
    required_guards: List[str] = field(default_factory=list)
    required_role: Optional[str] = None
    on_enter_hooks: List[str] = field(default_factory=list)
    on_exit_hooks: List[str] = field(default_factory=list)
    
    def __hash__(self):
        return hash((self.from_state, self.to_state))
    
    def __eq__(self, other):
        if not isinstance(other, TransitionInfo):
            return False
        return self.from_state == other.from_state and self.to_state == other.to_state


class TransitionType(Enum):
    """Types of transitions."""
    APPROVAL = "approval"              # Forward approval flow
    REJECTION = "rejection"            # Rejection flow
    CANCELLATION = "cancellation"      # User cancellation
    COMPLETION = "completion"          # Process completion
    ERROR_RECOVERY = "error_recovery"  # Recovery from error


class TransitionRegistry:
    """Registry of all possible transitions with metadata."""
    
    def __init__(self):
        """Initialize transition registry."""
        self.transitions: Dict[tuple, TransitionInfo] = {}
        self._setup_default_transitions()
    
    def _setup_default_transitions(self) -> None:
        """Setup default leave request transitions."""
        transitions = [
            # DRAFT transitions
            TransitionInfo(
                from_state="draft",
                to_state="submitted",
                name="submit",
                description="Employee submits leave request",
                required_guards=["valid_period"],
                on_enter_hooks=["validate_request"],
            ),
            TransitionInfo(
                from_state="draft",
                to_state="cancelled",
                name="cancel_draft",
                description="Employee cancels draft request",
                on_exit_hooks=["notify_cancellation"],
            ),
            
            # SUBMITTED transitions
            TransitionInfo(
                from_state="submitted",
                to_state="approved_mgr",
                name="approve_manager",
                description="Manager approves request",
                required_guards=["has_balance", "no_overlap", "coverage"],
                required_role="manager",
                on_enter_hooks=["notify_approval"],
            ),
            TransitionInfo(
                from_state="submitted",
                to_state="rejected",
                name="reject_manager",
                description="Manager rejects request",
                required_role="manager",
                on_enter_hooks=["notify_rejection"],
            ),
            TransitionInfo(
                from_state="submitted",
                to_state="cancelled",
                name="cancel_submitted",
                description="Employee cancels submitted request",
                on_enter_hooks=["notify_cancellation"],
            ),
            
            # APPROVED_MANAGER transitions
            TransitionInfo(
                from_state="approved_mgr",
                to_state="approved_hr",
                name="approve_hr",
                description="HR approves request",
                required_role="hr",
                on_enter_hooks=["allocate_leave_balance", "notify_approval"],
            ),
            TransitionInfo(
                from_state="approved_mgr",
                to_state="rejected",
                name="reject_hr",
                description="HR rejects request",
                required_role="hr",
                on_enter_hooks=["notify_rejection"],
            ),
            TransitionInfo(
                from_state="approved_mgr",
                to_state="cancelled",
                name="cancel_approved",
                description="Employee cancels approved request",
                on_enter_hooks=["restore_balance", "notify_cancellation"],
            ),
            
            # APPROVED_HR (Final) transitions
            TransitionInfo(
                from_state="approved_hr",
                to_state="completed",
                name="complete",
                description="Leave period ends",
                on_enter_hooks=["generate_summary"],
            ),
            TransitionInfo(
                from_state="approved_hr",
                to_state="cancelled",
                name="cancel_final",
                description="Employee cancels final approval",
                on_enter_hooks=["restore_balance", "notify_cancellation"],
            ),
            
            # Terminal state recovery
            TransitionInfo(
                from_state="failed",
                to_state="draft",
                name="recover",
                description="Recover from error state",
                on_enter_hooks=["reset_request"],
            ),
        ]
        
        for transition in transitions:
            self.register_transition(transition)
    
    def register_transition(self, transition: TransitionInfo) -> None:
        """
        Register a transition.
        
        Args:
            transition: TransitionInfo to register
        """
        key = (transition.from_state, transition.to_state)
        self.transitions[key] = transition
        logger.debug(f"Registered transition: {transition.from_state} → {transition.to_state}")
    
    def get_transition(
        self,
        from_state: str,
        to_state: str,
    ) -> Optional[TransitionInfo]:
        """
        Get transition information.
        
        Args:
            from_state: Current state
            to_state: Target state
            
        Returns:
            TransitionInfo or None
        """
        return self.transitions.get((from_state, to_state))
    
    def get_transitions_from(self, from_state: str) -> List[TransitionInfo]:
        """
        Get all transitions from a state.
        
        Args:
            from_state: Source state
            
        Returns:
            List of TransitionInfo
        """
        return [
            t for t in self.transitions.values()
            if t.from_state == from_state
        ]
    
    def get_transitions_to(self, to_state: str) -> List[TransitionInfo]:
        """
        Get all transitions to a state.
        
        Args:
            to_state: Target state
            
        Returns:
            List of TransitionInfo
        """
        return [
            t for t in self.transitions.values()
            if t.to_state == to_state
        ]
    
    def get_all_transitions(self) -> List[TransitionInfo]:
        """Get all registered transitions."""
        return list(self.transitions.values())
