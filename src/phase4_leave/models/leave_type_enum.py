# phase4_leave/models/leave_type_enum.py

from enum import Enum


class LeaveType(str, Enum):
    ANNUAL    = "annual"
    SICK      = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    UNPAID    = "unpaid"

    def display(self) -> str:
        labels = {
            "annual":    "Annual / Casual Leave",
            "sick":      "Sick Leave",
            "maternity": "Maternity Leave",
            "paternity": "Paternity Leave",
            "unpaid":    "Unpaid Leave",
        }
        return labels.get(self.value, self.value.title())


class LeaveRequestStatus(str, Enum):
    DRAFT               = "draft"
    SUBMITTED           = "submitted"
    PENDING_APPROVAL    = "pending_approval"
    APPROVED            = "approved"
    REJECTED            = "rejected"
    CANCELLED           = "cancelled"
    COMPLETED           = "completed"
    VOIDED              = "voided"


class ApprovalStatus(str, Enum):
    PENDING     = "pending"
    APPROVED    = "approved"
    REJECTED    = "rejected"
    WITHDRAWN   = "withdrawn"


class ApprovingAuthority(str, Enum):
    DIRECT_MANAGER      = "direct_manager"
    DEPARTMENT_HEAD     = "department_head"
    HR_MANAGER          = "hr_manager"
    EXECUTIVE           = "executive"
    SYSTEM              = "system"
