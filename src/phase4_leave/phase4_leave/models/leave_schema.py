# phase4_leave/models/leave_policy_model.py

from dataclasses import dataclass
from typing import Optional
from .leave_type_enum import LeaveType


@dataclass(frozen=True)
class LeaveTypePolicy:
    leave_type:            LeaveType
    max_days_per_request:  int
    max_days_per_year:     int
    min_notice_days:       int
    requires_document:     bool
    carries_forward:       bool
    paid:                  bool
    eligible_genders:      Optional[list[str]]
    min_tenure_days:       int
    cooldown_days:         int
    can_overlap_team:      bool
    max_team_overlap_pct:  float
    accrual_per_month:     float
    description:           str = ""