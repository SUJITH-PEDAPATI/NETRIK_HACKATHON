"""Comprehensive audit logging for escalation system."""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class AuditAction(str, Enum):
    """Types of auditable actions."""
    CASE_CREATED = "case_created"
    CASE_UPDATED = "case_updated"
    CASE_CLOSED = "case_closed"
    CASE_REOPENED = "case_reopened"
    CASE_ASSIGNED = "case_assigned"
    CASE_ESCALATED = "case_escalated"
    ANALYSIS_PERFORMED = "analysis_performed"
    RULE_MATCHED = "rule_matched"
    APPROVAL_GIVEN = "approval_given"
    APPROVAL_DENIED = "approval_denied"
    NOTIFICATION_SENT = "notification_sent"
    CONFIG_UPDATED = "config_updated"
    RULE_ADDED = "rule_added"
    RULE_UPDATED = "rule_updated"
    RULE_DELETED = "rule_deleted"
    DATA_ACCESSED = "data_accessed"
    DATA_EXPORTED = "data_exported"
    SYSTEM_EVENT = "system_event"
    ERROR_OCCURRED = "error_occurred"


class AuditSeverity(str, Enum):
    """Severity levels for audit events."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    ERROR = "error"
    SECURITY = "security"


@dataclass
class AuditEntry:
    """Single audit log entry."""
    
    entry_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    action: AuditAction = AuditAction.SYSTEM_EVENT
    severity: AuditSeverity = AuditSeverity.INFO
    actor_id: Optional[str] = None
    actor_role: Optional[str] = None
    actor_email: Optional[str] = None
    resource_type: Optional[str] = None  # 'case', 'rule', 'config'
    resource_id: Optional[str] = None
    old_values: Optional[Dict] = None
    new_values: Optional[Dict] = None
    change_summary: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: Optional[str] = None
    status: str = "success"  # success, failure
    error_message: Optional[str] = None
    additional_context: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'entry_id': self.entry_id,
            'timestamp': self.timestamp.isoformat(),
            'action': self.action.value,
            'severity': self.severity.value,
            'actor_id': self.actor_id,
            'actor_role': self.actor_role,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'change_summary': self.change_summary,
            'status': self.status,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class AuditLogger:
    """Centralized audit logging system."""
    
    def __init__(self, repository=None, enable_remote_logging: bool = False):
        """Initialize audit logger.
        
        Args:
            repository: Storage backend for logs
            enable_remote_logging: Send logs to remote service
        """
        self.repository = repository
        self.enable_remote_logging = enable_remote_logging
        self.local_buffer = []
        self.buffer_size = 100
        self.log_retention_days = 2555  # 7 years
    
    def log_action(
        self,
        action: AuditAction,
        actor_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        changes: Optional[Dict] = None,
        context: Optional[Dict] = None,
        severity: AuditSeverity = AuditSeverity.INFO
    ) -> str:
        """Log an action.
        
        Args:
            action: Action type
            actor_id: Who performed action
            resource_type: Type of resource
            resource_id: Resource ID
            changes: What changed
            context: Additional context
            severity: Event severity
            
        Returns:
            Entry ID
        """
        pass
    
    def log_case_event(
        self,
        case_id: str,
        action: AuditAction,
        actor_id: Optional[str] = None,
        old_state: Optional[Dict] = None,
        new_state: Optional[Dict] = None
    ) -> str:
        """Log case-related event."""
        pass
    
    def log_rule_event(
        self,
        rule_id: str,
        action: AuditAction,
        actor_id: Optional[str] = None,
        rule_data: Optional[Dict] = None
    ) -> str:
        """Log rule-related event."""
        pass
    
    def log_access(
        self,
        actor_id: str,
        resource_id: str,
        resource_type: str,
        access_type: str  # 'read', 'write', 'delete'
    ) -> str:
        """Log data access."""
        pass
    
    def log_analysis(
        self,
        content_hash: str,
        escalation_triggered: bool,
        escalation_level: Optional[str] = None,
        matching_rules: Optional[List[str]] = None
    ) -> str:
        """Log escalation analysis."""
        pass
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict] = None,
        actor_id: Optional[str] = None
    ) -> str:
        """Log system error."""
        pass
    
    def get_logs(
        self,
        filters: Optional[Dict] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditEntry]:
        """Retrieve logs with filters."""
        pass
    
    def get_case_logs(self, case_id: str) -> List[AuditEntry]:
        """Get all logs for a case."""
        pass
    
    def get_actor_logs(self, actor_id: str) -> List[AuditEntry]:
        """Get all logs for an actor."""
        pass
    
    def generate_audit_report(
        self,
        start_date: datetime,
        end_date: datetime,
        format: str = 'json'
    ) -> str:
        """Generate audit report."""
        pass
    
    def purge_old_logs(self, older_than_days: int = None):
        """Delete old audit logs."""
        pass
    
    def get_suspicious_activities(self, threshold_hours: int = 24) -> List[AuditEntry]:
        """Detect suspicious activity patterns."""
        pass
    
    def _buffer_entry(self, entry: AuditEntry):
        """Buffer log entry for batch writing."""
        pass
    
    def _flush_buffer(self):
        """Write buffered entries to storage."""
        pass
