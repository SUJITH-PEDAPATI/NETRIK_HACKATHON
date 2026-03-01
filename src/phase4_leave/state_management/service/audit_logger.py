"""
state_management/service/audit_logger.py

Audit logging and tracking for leave requests.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class AuditAction(Enum):
    """Audit action types."""
    CREATED = "created"
    TRANSITIONED = "transitioned"
    GUARD_FAILED = "guard_failed"
    HOOK_EXECUTED = "hook_executed"
    ERROR = "error"


@dataclass
class AuditEntry:
    """Single audit log entry."""
    timestamp: datetime
    request_id: str
    action: AuditAction
    user_id: Optional[str] = None
    user_role: Optional[str] = None
    from_state: Optional[str] = None
    to_state: Optional[str] = None
    details: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.request_id,
            "action": self.action.value,
            "user_id": self.user_id,
            "user_role": self.user_role,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "details": self.details,
        }


class AuditLogger:
    """Comprehensive audit logger for leave management."""
    
    def __init__(self):
        """Initialize audit logger."""
        self.entries: List[AuditEntry] = []
    
    def log_creation(self, request_id: str, creator_id: str) -> None:
        """
        Log request creation.
        
        Args:
            request_id: Request ID
            creator_id: User who created request
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            request_id=request_id,
            action=AuditAction.CREATED,
            user_id=creator_id,
            details={
                "event": "Leave request created",
            }
        )
        self.entries.append(entry)
        logger.info(f"Audit: Request {request_id} created by {creator_id}")
    
    def log_transition(self, context) -> None:
        """
        Log state transition.
        
        Args:
            context: TransitionContext
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            request_id=context.request_id,
            action=AuditAction.TRANSITIONED,
            user_id=context.user_id,
            user_role=context.user_role,
            from_state=context.from_state,
            to_state=context.to_state,
            details={
                "reason": context.reason,
                "metadata": context.metadata,
            }
        )
        self.entries.append(entry)
        logger.info(f"Audit: {context.request_id} transitioned "
                   f"{context.from_state} → {context.to_state} by {context.user_id}")
    
    def log_guard_failure(
        self,
        request_id: str,
        guard_name: str,
        reason: str,
    ) -> None:
        """
        Log guard evaluation failure.
        
        Args:
            request_id: Request ID
            guard_name: Guard name
            reason: Failure reason
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            request_id=request_id,
            action=AuditAction.GUARD_FAILED,
            details={
                "guard": guard_name,
                "reason": reason,
            }
        )
        self.entries.append(entry)
        logger.warning(f"Audit: Guard failed for {request_id}: {guard_name} - {reason}")
    
    def log_hook_execution(
        self,
        request_id: str,
        hook_name: str,
        event_type: str,
        status: str,
    ) -> None:
        """
        Log hook execution.
        
        Args:
            request_id: Request ID
            hook_name: Hook name
            event_type: "enter" or "exit"
            status: "success" or "failed"
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            request_id=request_id,
            action=AuditAction.HOOK_EXECUTED,
            details={
                "hook": hook_name,
                "event_type": event_type,
                "status": status,
            }
        )
        self.entries.append(entry)
        logger.debug(f"Audit: Hook {hook_name} ({event_type}) - {status}")
    
    def log_error(
        self,
        request_id: str,
        error_msg: str,
        context: Optional[Dict] = None,
    ) -> None:
        """
        Log error.
        
        Args:
            request_id: Request ID
            error_msg: Error message
            context: Additional context
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            request_id=request_id,
            action=AuditAction.ERROR,
            details={
                "error": error_msg,
                "context": context or {},
            }
        )
        self.entries.append(entry)
        logger.error(f"Audit: Error for {request_id}: {error_msg}")
    
    def get_request_history(self, request_id: str) -> List[AuditEntry]:
        """
        Get full audit history for a request.
        
        Args:
            request_id: Request ID
            
        Returns:
            List of audit entries
        """
        return [e for e in self.entries if e.request_id == request_id]
    
    def get_user_actions(self, user_id: str) -> List[AuditEntry]:
        """
        Get all actions by a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of audit entries
        """
        return [e for e in self.entries if e.user_id == user_id]
    
    def export_to_json(self, filepath: str) -> None:
        """
        Export audit log to JSON.
        
        Args:
            filepath: Output file path
        """
        data = [entry.to_dict() for entry in self.entries]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Audit log exported to {filepath}")
    
    def get_stats(self) -> Dict:
        """
        Get audit statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "total_entries": len(self.entries),
            "actions": {
                action.value: len([e for e in self.entries if e.action == action])
                for action in AuditAction
            },
            "unique_requests": len(set(e.request_id for e in self.entries)),
            "unique_users": len(set(e.user_id for e in self.entries if e.user_id)),
        }
