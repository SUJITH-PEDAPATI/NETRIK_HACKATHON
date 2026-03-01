"""
phase3_scheduling/models/types.py
─────────────────────────────────
Advanced type definitions for scheduling system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class InterviewType(Enum):
    """Types of interviews."""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    CULTURAL = "cultural"
    FINAL_ROUND = "final_round"


class InterviewStatus(Enum):
    """Status of interview."""
    PROPOSED = "proposed"
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"
    CANCELLED = "cancelled"


class SeniorityLevel(Enum):
    """Candidate seniority level."""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


@dataclass
class TimeSlot:
    """Represents a single time slot."""
    start_time: datetime
    end_time: datetime
    interviewer_id: Optional[str] = None
    
    def duration(self) -> timedelta:
        """Get slot duration."""
        return self.end_time - self.start_time
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this slot overlaps with another."""
        return (self.start_time < other.end_time and 
                self.end_time > other.start_time)


@dataclass
class Candidate:
    """Represents a candidate."""
    id: str
    name: str
    email: str
    availability: List[TimeSlot] = field(default_factory=list)
    interviews_needed: int = 1
    skills: List[str] = field(default_factory=list)
    seniority: str = "mid"
    match_score: float = 0.0
    metadata: Dict = field(default_factory=dict)


@dataclass
class Interviewer:
    """Represents an interviewer."""
    id: str
    name: str
    email: str
    availability: List[TimeSlot] = field(default_factory=list)
    specialties: List[str] = field(default_factory=list)
    max_interviews_per_day: int = 4
    interview_types: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class Interview:
    """Represents a scheduled interview."""
    id: str
    candidate_id: str
    interviewer_id: str
    interview_type: InterviewType
    scheduled_time: Optional[datetime] = None
    status: InterviewStatus = InterviewStatus.PROPOSED
    duration_minutes: int = 60
    location: Optional[str] = None
    notes: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class ScheduleConstraint:
    """Represents a scheduling constraint."""
    name: str
    constraint_type: str  # "hard" or "soft"
    description: str
    penalty: float = 1.0  # For soft constraints


@dataclass
class Schedule:
    """Complete interview schedule."""
    id: str
    created_at: datetime
    interviews: List[Interview] = field(default_factory=list)
    constraints: List[ScheduleConstraint] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def get_schedule_stats(self) -> Dict:
        """Get statistics about the schedule."""
        return {
            "total_interviews": len(self.interviews),
            "scheduled": len([i for i in self.interviews if i.status == InterviewStatus.SCHEDULED]),
            "confirmed": len([i for i in self.interviews if i.status == InterviewStatus.CONFIRMED]),
        }


@dataclass
class ConflictInfo:
    """Information about a scheduling conflict."""
    conflict_type: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    interviews_involved: List[str]
    description: str
    suggested_resolution: Optional[str] = None


@dataclass
class ScheduleMetrics:
    """Metrics about schedule quality."""
    total_interviews: int
    scheduled_interviews: int
    unscheduled_interviews: int
    success_rate: float
    conflict_count: int
    warning_count: int
    avg_interviewer_load: float
    peak_hour: Optional[int] = None
    solver_time_seconds: float = 0.0
