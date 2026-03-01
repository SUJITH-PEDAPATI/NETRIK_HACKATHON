"""
state_management/service/state_service.py

Runtime transition executor and state management service.
"""

from typing import Dict, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class TransitionContext:
    """Context for a state transition."""
    request_id: str
    from_state: str
    to_state: str
    user_id: str
    user_role: str
    timestamp: datetime = field(default_factory=datetime.now)
    reason: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    guard_results: Dict = field(default_factory=dict)


class StateService:
    """
    Runtime state transition executor.
    Orchestrates transitions, guards, and hooks.
    """
    
    def __init__(self, fsm, guard_registry, transition_registry, hook_registry, audit_logger):
        """
        Initialize state service.
        
        Args:
            fsm: Finite State Machine definition
            guard_registry: Guard conditions registry
            transition_registry: Transition metadata registry
            hook_registry: Event hooks registry
            audit_logger: Audit logger instance
        """
        self.fsm = fsm
        self.guard_registry = guard_registry
        self.transition_registry = transition_registry
        self.hook_registry = hook_registry
        self.audit_logger = audit_logger
        
        self.requests: Dict[str, Dict] = {}
    
    def create_request(self, request_data: Dict) -> str:
        """
        Create a new leave request in DRAFT state.
        
        Args:
            request_data: Request data
            
        Returns:
            Request ID
        """
        request_id = request_data.get("request_id")
        
        request = {
            "request_id": request_id,
            "state": "draft",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "created_by": request_data.get("employee_id"),
            **request_data
        }
        
        self.requests[request_id] = request
        
        # Audit
        self.audit_logger.log_creation(request_id, request_data.get("employee_id"))
        
        logger.info(f"Created leave request: {request_id}")
        return request_id
    
    def can_transition(
        self,
        request_id: str,
        to_state: str,
        user_id: str,
        user_role: str,
        context_data: Optional[Dict] = None,
    ) -> tuple[bool, List[str]]:
        """
        Check if transition is allowed.
        
        Args:
            request_id: Request ID
            to_state: Target state
            user_id: User ID performing transition
            user_role: User role
            context_data: Additional context for guards
            
        Returns:
            (is_allowed, reasons_if_not)
        """
        request = self.requests.get(request_id)
        if not request:
            return False, ["Request not found"]
        
        from_state = request["state"]
        
        # Check FSM validity
        if not self.fsm.is_valid_transition(from_state, to_state):
            return False, [f"Invalid transition: {from_state} → {to_state}"]
        
        # Get transition info
        transition = self.transition_registry.get_transition(from_state, to_state)
        if not transition:
            return False, ["Transition not configured"]
        
        reasons = []
        
        # Check role requirement
        if transition.required_role and user_role != transition.required_role:
            reasons.append(f"Requires role: {transition.required_role}")
        
        # Evaluate guards
        if transition.required_guards:
            context_data = context_data or {}
            for guard_name in transition.required_guards:
                result = self.guard_registry.evaluate_guard(
                    guard_name,
                    request,
                    context_data,
                )
                if not result.allowed:
                    reasons.append(result.reason)
        
        return len(reasons) == 0, reasons
    
    def transition(
        self,
        request_id: str,
        to_state: str,
        user_id: str,
        user_role: str,
        reason: Optional[str] = None,
        context_data: Optional[Dict] = None,
    ) -> tuple[bool, Optional[str]]:
        """
        Execute a state transition.
        
        Args:
            request_id: Request ID
            to_state: Target state
            user_id: User ID
            user_role: User role
            reason: Transition reason
            context_data: Context for guards
            
        Returns:
            (success, error_message)
        """
        # Check if transition is allowed
        allowed, reasons = self.can_transition(
            request_id,
            to_state,
            user_id,
            user_role,
            context_data,
        )
        
        if not allowed:
            error_msg = "; ".join(reasons)
            logger.warning(f"Transition denied: {error_msg}")
            return False, error_msg
        
        request = self.requests[request_id]
        from_state = request["state"]
        transition = self.transition_registry.get_transition(from_state, to_state)
        
        # Create context
        ctx = TransitionContext(
            request_id=request_id,
            from_state=from_state,
            to_state=to_state,
            user_id=user_id,
            user_role=user_role,
            reason=reason,
            metadata=context_data or {},
        )
        
        try:
            # Pre-transition: Exit hooks
            if transition.on_exit_hooks:
                for hook_name in transition.on_exit_hooks:
                    self.hook_registry.execute_hook(hook_name, "exit", ctx, request)
            
            # Update state
            request["state"] = to_state
            request["updated_at"] = datetime.now().isoformat()
            request["updated_by"] = user_id
            
            # Post-transition: Enter hooks
            if transition.on_enter_hooks:
                for hook_name in transition.on_enter_hooks:
                    self.hook_registry.execute_hook(hook_name, "enter", ctx, request)
            
            # Audit
            self.audit_logger.log_transition(ctx)
            
            logger.info(f"Transition completed: {request_id} {from_state} → {to_state}")
            return True, None
            
        except Exception as e:
            logger.error(f"Transition failed: {e}")
            # Mark as failed
            request["state"] = "failed"
            request["error"] = str(e)
            return False, f"Transition error: {e}"
    
    def get_request(self, request_id: str) -> Optional[Dict]:
        """Get request details."""
        return self.requests.get(request_id)
    
    def get_requests_by_state(self, state: str) -> List[Dict]:
        """Get all requests in a state."""
        return [r for r in self.requests.values() if r["state"] == state]
    
    def get_requests_by_employee(self, employee_id: str) -> List[Dict]:
        """Get all requests by employee."""
        return [r for r in self.requests.values() if r["employee_id"] == employee_id]
