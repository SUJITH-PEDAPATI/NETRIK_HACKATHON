# phase4_leave/models/leave_request_model.py

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from .leave_type_enum import LeaveType, LeaveRequestStatus, ApprovalStatus, ApprovingAuthority


@dataclass
class LeaveRequest:
    """Advanced leave request model with full lifecycle tracking."""
    
    request_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: date
    end_date: date
    status: LeaveRequestStatus = LeaveRequestStatus.DRAFT
    reason: Optional[str] = None
    supporting_documents: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    approval_chain: List['ApprovalNode'] = field(default_factory=list)
    contact_during_leave: Optional[str] = None
    relief_officer_id: Optional[str] = None
    handover_notes: Optional[str] = None
    version: int = 1
    metadata: dict = field(default_factory=dict)
    
    def get_duration_days(self) -> int:
        """Calculate total leave duration."""
        return (self.end_date - self.start_date).days + 1
    
    def is_pending_approval(self) -> bool:
        """Check if request is waiting for approval."""
        return self.status == LeaveRequestStatus.PENDING_APPROVAL
    
    def is_approved(self) -> bool:
        """Check if request has been approved."""
        return self.status == LeaveRequestStatus.APPROVED
    
    def is_rejected(self) -> bool:
        """Check if request has been rejected."""
        return self.status == LeaveRequestStatus.REJECTED
    
    def get_pending_approvals(self) -> List['ApprovalNode']:
        """Get approvals still pending."""
        return [node for node in self.approval_chain if node.status == ApprovalStatus.PENDING]


@dataclass
class ApprovalNode:
    """Single approval step in the workflow."""
    
    approval_id: str
    request_id: str
    approver_id: str
    authority_level: ApprovingAuthority
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    responded_at: Optional[datetime] = None
    comments: Optional[str] = None
    approval_order: int = 1
    is_optional: bool = False
    
    def is_approved(self) -> bool:
        """Check if this approval step is approved."""
        return self.status == ApprovalStatus.APPROVED
    
    def is_rejected(self) -> bool:
        """Check if this approval step has been rejected."""
        return self.status == ApprovalStatus.REJECTED


@dataclass
class LeaveAuditLog:
    """Audit trail for leave request changes."""
    
    log_id: str
    request_id: str
    employee_id: str
    action: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    performed_by: Optional[str] = None
    performed_at: datetime = field(default_factory=datetime.now)
    ip_address: Optional[str] = None
    additional_info: dict = field(default_factory=dict)
