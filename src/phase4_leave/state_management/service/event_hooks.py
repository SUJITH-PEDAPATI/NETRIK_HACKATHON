"""
state_management/service/event_hooks.py

Event hooks for lifecycle events in transitions.
"""

from typing import Dict, Callable, Optional, List
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class EventHook(ABC):
    """Base class for event hooks."""
    
    @abstractmethod
    def execute(self, event_type: str, context: Dict, request: Dict) -> None:
        """
        Execute the hook.
        
        Args:
            event_type: "enter" or "exit"
            context: TransitionContext
            request: Leave request object
        """
        pass


class ValidateRequestHook(EventHook):
    """Hook to validate request on submission."""
    
    def execute(self, event_type: str, context: Dict, request: Dict) -> None:
        if event_type == "enter":
            logger.info(f"Validating request {context.get('request_id')}")
            # Validation logic
            if not request.get("reason"):
                raise ValueError("Reason is required")


class NotifyApprovalHook(EventHook):
    """Hook to notify stakeholders of approval."""
    
    def execute(self, event_type: str, context: Dict, request: Dict) -> None:
        if event_type == "enter":
            request_id = context.get("request_id")
            employee_id = request.get("employee_id")
            logger.info(f"Notifying approval for {request_id} to {employee_id}")
            # Send notification


class NotifyRejectionHook(EventHook):
    """Hook to notify of rejection."""
    
    def execute(self, event_type: str, context: Dict, request: Dict) -> None:
        if event_type == "enter":
            request_id = context.get("request_id")
            employee_id = request.get("employee_id")
            logger.info(f"Notifying rejection for {request_id} to {employee_id}")
            # Send notification


class AllocateLeaveBalanceHook(EventHook):
    """Hook to allocate leave balance."""
    
    def execute(self, event_type: str, context: Dict, request: Dict) -> None:
        if event_type == "enter":
            logger.info(f"Allocating leave balance for {request.get('request_id')}")
            # Update balance


class RestoreBalanceHook(EventHook):
    """Hook to restore leave balance on cancellation."""
    
    def execute(self, event_type: str, context: Dict, request: Dict) -> None:
        if event_type == "enter":
            logger.info(f"Restoring leave balance for {request.get('request_id')}")
            # Restore balance


class HookRegistry:
    """Registry of event hooks."""
    
    def __init__(self):
        """Initialize hook registry."""
        self.hooks: Dict[str, EventHook] = {
            "validate_request": ValidateRequestHook(),
            "notify_approval": NotifyApprovalHook(),
            "notify_rejection": NotifyRejectionHook(),
            "allocate_leave_balance": AllocateLeaveBalanceHook(),
            "restore_balance": RestoreBalanceHook(),
            "notify_cancellation": NotifyApprovalHook(),  # Reuse approval hook
            "generate_summary": ValidateRequestHook(),    # Placeholder
            "reset_request": ValidateRequestHook(),       # Placeholder
        }
    
    def register_hook(self, name: str, hook: EventHook) -> None:
        """
        Register a hook.
        
        Args:
            name: Hook name
            hook: Hook implementation
        """
        self.hooks[name] = hook
        logger.info(f"Registered hook: {name}")
    
    def execute_hook(
        self,
        hook_name: str,
        event_type: str,
        context: Dict,
        request: Dict,
    ) -> None:
        """
        Execute a hook.
        
        Args:
            hook_name: Hook name
            event_type: "enter" or "exit"
            context: Transition context
            request: Leave request
        """
        hook = self.hooks.get(hook_name)
        if not hook:
            logger.warning(f"Hook not found: {hook_name}")
            return
        
        try:
            hook.execute(event_type, context, request)
        except Exception as e:
            logger.error(f"Hook execution failed ({hook_name}): {e}")
            raise
