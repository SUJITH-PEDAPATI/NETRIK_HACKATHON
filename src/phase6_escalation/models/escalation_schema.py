"""Data models for escalation requests and responses."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict
from .escalation_types import (
    EscalationCategory,
    EscalationReason,
    EscalationSeverity,
    ReportingChannel,
    HandlingDepartment,
    FollowUpAction
)


@dataclass
class EscalationRequest:
    """Incoming escalation request."""
    
    escalation_id: str
    reported_by_id: Optional[str]
    subject: str
    description: str
    category: EscalationCategory
    reason: EscalationReason
    reported_against_id: Optional[str] = None
    reporting_channel: ReportingChannel = ReportingChannel.INTERNAL_SYSTEM
    department_id: Optional[str] = None
    location: Optional[str] = None
    occurred_on: Optional[datetime] = None
    reported_on: datetime = field(default_factory=datetime.now)
    is_anonymous: bool = False
    attachments: List[str] = field(default_factory=list)
    additional_info: Dict = field(default_factory=dict)


@dataclass
class EscalationCase:
    """Complete escalation case record."""
    
    case_id: str
    escalation_request: EscalationRequest
    severity: EscalationSeverity
    confidence_score: float
    auto_detected: bool
    detection_timestamp: datetime = field(default_factory=datetime.now)
    assigned_to: Optional[str] = None
    handling_department: HandlingDepartment = HandlingDepartment.HR
    status: str = "open"  # open, under_investigation, resolved, closed
    resolution_notes: Optional[str] = None
    assigned_timestamp: Optional[datetime] = None
    resolved_timestamp: Optional[datetime] = None
    sla_deadline: Optional[datetime] = None
    follow_up_actions: List[FollowUpAction] = field(default_factory=list)
    related_cases: List[str] = field(default_factory=list)
    version: int = 1
    metadata: Dict = field(default_factory=dict)
    
    def is_overdue(self) -> bool:
        """Check if case is overdue for SLA."""
        if self.sla_deadline:
            return datetime.now() > self.sla_deadline
        return False
    
    def get_age_hours(self) -> float:
        """Get case age in hours."""
        return (datetime.now() - self.detection_timestamp).total_seconds() / 3600


@dataclass
class EscalationNotification:
    """Notification about escalation."""
    
    notification_id: str
    case_id: str
    recipient_id: str
    recipient_type: str  # 'user', 'department', 'role'
    notification_type: str  # 'new_case', 'assignment', 'update', 'resolution'
    message: str
    priority: str = "normal"  # low, normal, high, urgent
    sent_at: datetime = field(default_factory=datetime.now)
    read_at: Optional[datetime] = None
    channels: List[str] = field(default_factory=list)  # email, sms, system
    is_acknowledged: bool = False


@dataclass
class EscalationResponse:
    """Response to an escalation request."""
    
    response_id: str
    case_id: str
    action_taken: str
    status_update: str
    assigned_department: HandlingDepartment
    next_steps: List[str]
    timeline_estimate: Optional[str] = None
    responsible_officer_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    attachments: List[str] = field(default_factory=list)


@dataclass
class EscalationAuditLog:
    """Audit log for escalation activities."""
    
    log_id: str
    case_id: str
    action: str
    performed_by: str
    timestamp: datetime = field(default_factory=datetime.now)
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    details: Dict = field(default_factory=dict)
    ip_address: Optional[str] = None
