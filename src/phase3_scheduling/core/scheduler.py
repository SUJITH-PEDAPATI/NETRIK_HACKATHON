"""
phase3_scheduling/core/scheduler.py
────────────────────────────────────
Advanced scheduling engine with multiple algorithm support.
"""

from datetime import datetime, timedelta, timeī
from typing import Dict, List, Optional, Tuple
import logging
import time as time_module

logger = logging.getLogger(__name__)


def schedule(matrix: Dict, solver_type: str = "hybrid") -> Dict:
    """
    Main scheduling orchestrator using selected algorithm.
    
    Args:
        matrix: Input data with candidates, interviewers, date_range
        solver_type: "csp", "greedy", or "hybrid"
        
    Returns:
        Schedule result with assignments, stats, and metadata
    """ī
    logger.info(f"Starting scheduling with solver: {solver_type}")
    start_time = time_module.time()
    
    scheduler = SchedulingEngine(matrix)
    
    if solver_type == "csp":
        result = scheduler.solve_with_csp()
    elif solver_type == "greedy":
        result = scheduler.solve_with_greedy()
    else:  # hybrid
        result = scheduler.solve_hybrid()
    
    elapsed = time_module.time() - start_time
    result["stats"]["solver_time_seconds"] = round(elapsed, 2)
    
    logger.info(f"Scheduling complete in {elapsed:.2f}s: {result['stats']['scheduled_count']} scheduled")
    return result


class SchedulingEngine:
    """Advanced scheduling engine with multiple algorithm support."""
    
    def __init__(self, matrix: Dict):
        """Initialize scheduling engine."""
        self.matrix = matrix
        self.candidates = matrix.get("candidates", [])
        self.interviewers = matrix.get("interviewers", [])
        self.date_range = matrix.get("date_range", {})
        
        self._generate_time_slots()
        
        logger.info(f"Initialized SchedulingEngine: {len(self.candidates)} candidates, "
                   f"{len(self.interviewers)} interviewers")
    
    def _generate_time_slots(self):
        """Generate all available time slots."""
        self.slots = []
        start_date = datetime.strptime(self.date_range["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(self.date_range["end_date"], "%Y-%m-%d")
        
        current = start_date
        while current <= end_date:
            for interviewer in self.interviewers:
                for time_range in interviewer.get("available_times", []):
                    start_h = int(time_range.split("-")[0].split(":")[0])
                    end_h = int(time_range.split("-")[1].split(":")[0])
                    for hour in range(start_h, end_h):
                        slot = {
                            "start": current.replace(hour=hour),
                            "end": current.replace(hour=hour+1),
                            "interviewer_id": interviewer["id"],
                        }
                        self.slots.append(slot)
            current += timedelta(days=1)
        
        logger.info(f"Generated {len(self.slots)} time slots")
    
    def solve_with_csp(self) -> Dict:
        """Solve using Constraint Satisfaction Problem approach."""
        logger.info("Solving with CSP approach")
        assignments = self._csp_backtrack({}, set())
        return self._format_result(assignments)
    
    def solve_with_greedy(self) -> Dict:
        """Solve using greedy algorithm."""
        logger.info("Solving with Greedy approach")
        assignments = self._greedy_solve()
        return self._format_result(assignments)
    
    def solve_hybrid(self) -> Dict:
        """Solve using hybrid approach (greedy + CSP refinement)."""
        logger.info("Solving with Hybrid approach")
        # Start with greedy solution
        assignments = self._greedy_solve()
        
        # Refine with CSP constraints
        unassigned = [c for c in self.candidates if c["id"] not in assignments]
        for candidate in unassigned:
            slot = self._find_best_slot(candidate, assignments)
            if slot:
                assignments[candidate["id"]] = slot
        
        return self._format_result(assignments)
    
    def _csp_backtrack(self, assignments: Dict, used_slots: set, depth: int = 0) -> Dict:
        """CSP backtracking algorithm."""
        if depth > 1000:
            return assignments
        
        unassigned = next((c for c in self.candidates if c["id"] not in assignments), None)
        if not unassigned:
            return assignments
        
        for slot in self.slots:
            slot_key = f"{slot['start']}_{slot['interviewer_id']}"
            
            if slot_key in used_slots:
                continue
            
            if self._is_valid_assignment(unassigned, slot, assignments):
                assignments[unassigned["id"]] = slot
                used_slots.add(slot_key)
                
                result = self._csp_backtrack(assignments, used_slots, depth + 1)
                if len(result) == len(self.candidates):
                    return result
                
                del assignments[unassigned["id"]]
                used_slots.remove(slot_key)
        
        return assignments
    
    def _greedy_solve(self) -> Dict:
        """Greedy scheduling algorithm."""
        assignments = {}
        used_slots = set()
        
        sorted_candidates = sorted(
            self.candidates,
            key=lambda x: (-x.get("rounds_needed", 1), -{"senior": 3, "mid": 2, "junior": 1}.get(x.get("seniority"), 1))
        )
        
        for candidate in sorted_candidates:
            best_slot = None
            best_score = -1
            
            for slot in self.slots:
                slot_key = f"{slot['start']}_{slot['interviewer_id']}"
                if slot_key not in used_slots:
                    score = self._score_slot(candidate, slot)
                    if score > best_score:
                        best_score = score
                        best_slot = (slot, slot_key)
            
            if best_slot:
                slot, slot_key = best_slot
                assignments[candidate["id"]] = slot
                used_slots.add(slot_key)
        
        return assignments
    
    def _find_best_slot(self, candidate: Dict, assignments: Dict) -> Optional[Dict]:
        """Find best available slot for a candidate."""
        best_slot = None
        best_score = -1
        used_slots = {f"{a['start']}_{a['interviewer_id']}" for a in assignments.values()}
        
        for slot in self.slots:
            slot_key = f"{slot['start']}_{slot['interviewer_id']}"
            if slot_key not in used_slots and self._is_valid_assignment(candidate, slot, assignments):
                score = self._score_slot(candidate, slot)
                if score > best_score:
                    best_score = score
                    best_slot = slot
        
        return best_slot
    
    def _is_valid_assignment(self, candidate: Dict, slot: Dict, assignments: Dict) -> bool:
        """Check if assignment is valid."""
        interviewer_id = slot["interviewer_id"]
        interviewer = next((i for i in self.interviewers if i["id"] == interviewer_id), None)
        if not interviewer:
            return False
        
        slot_date = slot["start"].date()
        day_count = sum(1 for a in assignments.values() 
                       if a["interviewer_id"] == interviewer_id and a["start"].date() == slot_date)
        if day_count >= interviewer.get("max_per_day", 4):
            return False
        
        return True
    
    def _score_slot(self, candidate: Dict, slot: Dict) -> float:
        """Score a slot for a candidate."""
        score = 0.0
        
        slot_hour = slot["start"].hour
        preferred = candidate.get("preferred_times", [])
        for time_range in preferred:
            start_h = int(time_range.split("-")[0].split(":")[0])
            end_h = int(time_range.split("-")[1].split(":")[0])
            if start_h <= slot_hour < end_h:
                score += 10
        
        interviewer_id = slot["interviewer_id"]
        interviewer = next((i for i in self.interviewers if i["id"] == interviewer_id), None)
        if interviewer:
            cand_skills = set(candidate.get("skills", []))
            int_skills = set(interviewer.get("specialties", []))
            overlap = len(cand_skills & int_skills)
            score += overlap * 5
        
        score += {"junior": 3, "mid": 2, "senior": 1}.get(candidate.get("seniority"), 1)
        
        return score
    
    def _format_result(self, assignments: Dict) -> Dict:
        """Format assignments into result structure."""
        total = len(self.candidates)
        scheduled = len(assignments)
        
        interviews = []
        for cand_id, slot in assignments.items():
            cand = next((c for c in self.candidates if c["id"] == cand_id), None)
            interviews.append({
                "candidate_id": cand_id,
                "candidate_name": cand.get("name") if cand else "Unknown",
                "interviewer_id": slot["interviewer_id"],
                "start_time": slot["start"].isoformat(),
                "end_time": slot["end"].isoformat(),
                "duration_minutes": 60,
            })
        
        return {
            "interviews": interviews,
            "assignments": assignments,
            "stats": {
                "total_variables": total,
                "scheduled_count": scheduled,
                "unscheduled_count": total - scheduled,
                "success_rate": round(100 * scheduled / total, 1),
                "solver_time_seconds": 0,
            },
        }


class Scheduler:
    """Main scheduler interface."""
    
    def __init__(self, solver_type: str = "csp"):
        """
        Initialize scheduler.
        
        Args:
            solver_type: Type of solver ("csp" or "greedy")
        """
        self.solver_type = solver_type
        logger.info(f"Initialized Scheduler with solver: {solver_type}")
    
    def schedule(self, candidates: List[Dict], interviewers: List[Dict]) -> Dict:
        """
        Generate interview schedule.
        
        Args:
            candidates: List of candidate availability data
            interviewers: List of interviewer availability data
            
        Returns:
            Generated schedule dictionary
        """
        raise NotImplementedError()
    
    def validate_schedule(self, schedule: Dict) -> bool:
        """Validate the generated schedule."""
        raise NotImplementedError()
