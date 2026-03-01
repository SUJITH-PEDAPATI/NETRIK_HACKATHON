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