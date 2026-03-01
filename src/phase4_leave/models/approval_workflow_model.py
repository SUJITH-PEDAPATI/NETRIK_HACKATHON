# phase4_leave/models/approval_workflow_model.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Callable
from enum import Enum
from .leave_type_enum import LeaveType, ApprovingAuthority


class WorkflowState(str, Enum):
    CREATED      = "created"
    SUBMITTED    = "submitted"
    IN_PROGRESS  = "in_progress"
    COMPLETED    = "completed"
    FAILED       = "failed"
    CANCELLED    = "cancelled"


class TransitionType(str, Enum):
    AUTO        = "auto"
    MANUAL      = "manual"
    CONDITIONAL = "conditional"


@dataclass
class WorkflowTransition:
    """Represents a transition in the approval workflow."""
    
    from_state: WorkflowState
    to_state: WorkflowState
    transition_type: TransitionType
    requires_approver: bool = False
    approver_authority: Optional[ApprovingAuthority] = None
    condition_check: Optional[Callable] = None
    on_transition_hook: Optional[Callable] = None
    allowed_roles: List[str] = field(default_factory=list)


@dataclass
class ApprovalWorkflowConfig:
    """Configuration for approval workflows by leave type."""
    
    leave_type: LeaveType
    workflow_name: str
    description: str
    sequential_approval: bool = True
    parallel_approval: bool = False
    min_approvers_required: int = 1
    max_days_auto_approve: float = 5.0
    auto_approve_leave_types: List[LeaveType] = field(default_factory=list)
    escalation_days: int = 3
    requires_supporting_docs: bool = False
    required_doc_types: List[str] = field(default_factory=list)
    transitions: List[WorkflowTransition] = field(default_factory=list)
    notification_config: dict = field(default_factory=dict)
    sla_hours: int = 48
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


@dataclass
class WorkflowNotification:
    """Notification configuration for workflow events."""
    
    notification_id: str
    event_type: str
    recipient_id: str
    recipient_type: str  # 'employee', 'approver', 'manager'
    notification_method: str  # 'email', 'sms', 'system'
    subject: str
    message_template: str
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    enabled: bool = True
