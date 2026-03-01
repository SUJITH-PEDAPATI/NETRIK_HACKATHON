"""
phase3_scheduling/core/conflict_analysis.py
──────────────────────────────────────────────
Advanced conflict detection and resolution.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def analyse_conflicts(result: Dict) -> Dict:
    """
    Analyze scheduling result for conflicts.
    
    Args:
        result: Scheduling result from scheduler
        
    Returns:
        Conflict analysis report
    """
    analyzer = ConflictAnalyzer(result)
    return analyzer.analyze()


class ConflictAnalyzer:
    """Analyzes and reports scheduling conflicts."""
    
    def __init__(self, result: Dict = None):
        """Initialize conflict analyzer."""
        self.result = result or {}
        self.interviews = result.get("interviews", []) if result else []
        self.conflicts = []
        self.warnings = []
        logger.info("Initialized ConflictAnalyzer")
    
    def analyze(self) -> Dict:
        """Perform comprehensive conflict analysis."""
        logger.info(f"Analyzing {len(self.interviews)} interviews for conflicts")
        
        self._detect_time_conflicts()
        self._detect_interviewer_overload()
        self._detect_candidate_conflicts()
        self._detect_skill_mismatches()
        
        is_conflict_free = len(self.conflicts) == 0
        logger.info(f"Conflict analysis complete: {len(self.conflicts)} conflicts")
        
        return {
            "is_conflict_free": is_conflict_free,
            "conflicts": self.conflicts,
            "warnings": self.warnings,
            "total_conflicts": len(self.conflicts),
            "total_warnings": len(self.warnings),
            "severity_breakdown": self._get_severity_breakdown(),
        }
    
    def find_conflicts(self, schedule: Dict) -> List[Dict]:
        """
        Find all conflicts in a schedule.
        
        Args:
            schedule: Schedule to analyze
            
        Returns:
            List of conflict dictionaries
        """
        self.interviews = schedule.get("interviews", [])
        self._detect_time_conflicts()
        self._detect_interviewer_overload()
        return self.conflicts
    
    def _detect_time_conflicts(self):
        """Detect overlapping time slots."""
        for i, interview1 in enumerate(self.interviews):
            for interview2 in self.interviews[i+1:]:
                if interview1["interviewer_id"] == interview2["interviewer_id"]:
                    t1_start = datetime.fromisoformat(interview1["start_time"])
                    t1_end = datetime.fromisoformat(interview1["end_time"])
                    t2_start = datetime.fromisoformat(interview2["start_time"])
                    t2_end = datetime.fromisoformat(interview2["end_time"])
                    
                    if t1_start < t2_end and t1_end > t2_start:
                        self.conflicts.append({
                            "type": "TIME_CONFLICT",
                            "severity": "CRITICAL",
                            "interviews": [interview1["candidate_id"], interview2["candidate_id"]],
                            "interviewer": interview1["interviewer_id"],
                            "message": f"Time overlap: {interview1['candidate_name']} and "
                                      f"{interview2['candidate_name']}",
                        })
    
    def _detect_interviewer_overload(self):
        """Detect interviewer overload."""
        interviewer_load = {}
        for interview in self.interviews:
            int_id = interview["interviewer_id"]
            day = datetime.fromisoformat(interview["start_time"]).date()
            key = f"{int_id}_{day}"
            interviewer_load[key] = interviewer_load.get(key, 0) + 1
        
        for key, count in interviewer_load.items():
            if count > 5:
                self.warnings.append({
                    "type": "OVERLOAD",
                    "severity": "HIGH",
                    "interviewer": key.split("_")[0],
                    "count": count,
                    "message": f"Interviewer has {count} interviews in a day",
                })
    
    def _detect_candidate_conflicts(self):
        """Detect candidate scheduling issues."""
        candidate_interviews = {}
        for interview in self.interviews:
            cand_id = interview["candidate_id"]
            if cand_id not in candidate_interviews:
                candidate_interviews[cand_id] = []
            candidate_interviews[cand_id].append(interview)
        
        for cand_id, interviews in candidate_interviews.items():
            if len(interviews) > 1:
                for i, int1 in enumerate(interviews):
                    for int2 in interviews[i+1:]:
                        t1_start = datetime.fromisoformat(int1["start_time"])
                        t1_end = datetime.fromisoformat(int1["end_time"])
                        t2_start = datetime.fromisoformat(int2["start_time"])
                        t2_end = datetime.fromisoformat(int2["end_time"])
                        
                        gap = (t2_start - t1_end).total_seconds() / 3600
                        if gap < 1:
                            self.warnings.append({
                                "type": "TIGHT_SCHEDULE",
                                "candidate": cand_id,
                                "gap_hours": round(gap, 1),
                                "message": f"Only {gap:.1f}h gap between interviews",
                            })
    
    def _detect_skill_mismatches(self):
        """Detect potential skill mismatches."""
        pass
    
    def _get_severity_breakdown(self) -> Dict:
        """Get breakdown of conflict severities."""
        breakdown = {
            "CRITICAL": len([c for c in self.conflicts if c.get("severity") == "CRITICAL"]),
            "HIGH": len([c for c in self.conflicts if c.get("severity") == "HIGH"]),
            "MEDIUM": len([c for c in self.conflicts if c.get("severity") == "MEDIUM"]),
            "LOW": len([c for c in self.conflicts if c.get("severity") == "LOW"]),
        }
        return breakdown
    
    def resolve_conflicts(self, schedule: Dict, conflicts: List[Dict]) -> Dict:
        """Attempt to resolve conflicts."""
        raise NotImplementedError()
    
    def generate_conflict_report(self, conflicts: List[Dict]) -> str:
        """Generate a readable conflict report."""
        raise NotImplementedError()
