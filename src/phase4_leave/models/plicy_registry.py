# phase4_leave/models/policy_registry.py

from .leave_type_enum import LeaveType
from .leave_policy_model import LeaveTypePolicy


LEAVE_POLICIES: dict[LeaveType, LeaveTypePolicy] = {

    LeaveType.ANNUAL: LeaveTypePolicy(
        leave_type           = LeaveType.ANNUAL,
        max_days_per_request = 15,
        max_days_per_year    = 21,
        min_notice_days      = 7,
        requires_document    = False,
        carries_forward      = True,
        paid                 = True,
        eligible_genders     = None,
        min_tenure_days      = 90,
        cooldown_days        = 0,
        can_overlap_team     = False,
        max_team_overlap_pct = 0.30,
        accrual_per_month    = 1.75,
        description          = "Standard paid annual / casual leave.",
    ),

    LeaveType.SICK: LeaveTypePolicy(
        leave_type           = LeaveType.SICK,
        max_days_per_request = 7,
        max_days_per_year    = 12,
        min_notice_days      = 0,
        requires_document    = False,
        carries_forward      = False,
        paid                 = True,
        eligible_genders     = None,
        min_tenure_days      = 0,
        cooldown_days        = 0,
        can_overlap_team     = True,
        max_team_overlap_pct = 1.0,
        accrual_per_month    = 1.0,
        description          = "Paid sick leave. Medical cert required if > 3 days.",
    ),

    LeaveType.MATERNITY: LeaveTypePolicy(
        leave_type           = LeaveType.MATERNITY,
        max_days_per_request = 182,
        max_days_per_year    = 182,
        min_notice_days      = 30,
        requires_document    = True,
        carries_forward      = False,
        paid                 = True,
        eligible_genders     = ["F"],
        min_tenure_days      = 180,
        cooldown_days        = 365,
        can_overlap_team     = True,
        max_team_overlap_pct = 1.0,
        accrual_per_month    = 0.0,
        description          = "Statutory maternity leave.",
    ),

    LeaveType.PATERNITY: LeaveTypePolicy(
        leave_type           = LeaveType.PATERNITY,
        max_days_per_request = 15,
        max_days_per_year    = 15,
        min_notice_days      = 14,
        requires_document    = True,
        carries_forward      = False,
        paid                 = True,
        eligible_genders     = ["M"],
        min_tenure_days      = 180,
        cooldown_days        = 365,
        can_overlap_team     = True,
        max_team_overlap_pct = 1.0,
        accrual_per_month    = 0.0,
        description          = "Paid paternity leave.",
    ),

    LeaveType.UNPAID: LeaveTypePolicy(
        leave_type           = LeaveType.UNPAID,
        max_days_per_request = 90,
        max_days_per_year    = 90,
        min_notice_days      = 14,
        requires_document    = False,
        carries_forward      = False,
        paid                 = False,
        eligible_genders     = None,
        min_tenure_days      = 365,
        cooldown_days        = 180,
        can_overlap_team     = False,
        max_team_overlap_pct = 0.20,
        accrual_per_month    = 0.0,
        description          = "Unpaid leave of absence.",
    ),
}