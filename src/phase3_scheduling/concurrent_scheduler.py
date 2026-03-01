"""
Concurrent Scheduling Optimizer
Parallelizes resource-intensive scheduling operations
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)


@dataclass
class SchedulingParams:
    """Parameters for a scheduling task"""
    interviewer_id: str
    candidate_id: str
    preferred_slots: List[Tuple[str, str]]  # [(date, time), ...]
    constraints: Dict[str, Any]
    duration_minutes: int = 60


class ConcurrentScheduler:
    """
    Parallel scheduler for generating conflict-free interview schedules
    Uses thread pool to check multiple schedule hypotheses simultaneously
    """
    
    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def schedule_batch(
        self,
        scheduling_params: List[SchedulingParams],
        conflict_checker_fn,
        scheduler_fn
    ) -> Dict[str, Any]:
        """
        Schedule multiple interviews in parallel
        
        Args:
            scheduling_params: List of scheduling tasks
            conflict_checker_fn: Function to check conflicts
            scheduler_fn: Function to find optimal slot
        
        Returns:
            Dict with scheduled and failed counts
        """
        self.logger.info(f"Scheduling {len(scheduling_params)} interviews with {self.max_workers} threads")
        start_time = time.time()
        
        scheduled = []
        failed = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="Scheduler") as executor:
            futures = {
                executor.submit(
                    self._schedule_single,
                    params,
                    conflict_checker_fn,
                    scheduler_fn
                ): params.candidate_id
                for params in scheduling_params
            }
            
            for future in as_completed(futures):
                candidate_id = futures[future]
                try:
                    result = future.result(timeout=30)
                    if result["success"]:
                        scheduled.append(result)
                    else:
                        failed.append(result)
                except Exception as e:
                    failed.append({
                        "candidate_id": candidate_id,
                        "success": False,
                        "error": str(e)
                    })
        
        elapsed = time.time() - start_time
        
        self.logger.info(
            f"Scheduling complete: {len(scheduled)} scheduled, "
            f"{len(failed)} failed in {elapsed:.2f}s"
        )
        
        return {
            "total": len(scheduling_params),
            "scheduled": len(scheduled),
            "failed": len(failed),
            "results": scheduled,
            "failures": failed,
            "duration_seconds": elapsed
        }
    
    @staticmethod
    def _schedule_single(
        params: SchedulingParams,
        conflict_checker_fn,
        scheduler_fn
    ) -> Dict[str, Any]:
        """Schedule a single interview (task function)"""
        try:
            # Check for conflicts in preferred slots
            available_slots = [
                slot for slot in params.preferred_slots
                if not conflict_checker_fn(params.interviewer_id, slot)
            ]
            
            if not available_slots:
                return {
                    "candidate_id": params.candidate_id,
                    "success": False,
                    "error": "No available slots"
                }
            
            # Find optimal slot
            optimal_slot = scheduler_fn(
                params.candidate_id,
                available_slots,
                params.constraints
            )
            
            return {
                "candidate_id": params.candidate_id,
                "interviewer_id": params.interviewer_id,
                "scheduled_slot": optimal_slot,
                "success": True
            }
        except Exception as e:
            return {
                "candidate_id": params.candidate_id,
                "success": False,
                "error": str(e)
            }
    
    def parallel_conflict_analysis(
        self,
        schedule: List[Dict],
        conflict_detector_fn
    ) -> Dict[str, Any]:
        """
        Analyze conflicts across entire schedule in parallel
        """
        self.logger.info(f"Analyzing conflicts for {len(schedule)} slots")
        
        conflicts = []
        
        # Check each pair for conflicts
        slot_pairs = [
            (schedule[i], schedule[j])
            for i in range(len(schedule))
            for j in range(i + 1, len(schedule))
        ]
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(conflict_detector_fn, slot1, slot2): (slot1["id"], slot2["id"])
                for slot1, slot2 in slot_pairs
            }
            
            for future in as_completed(futures):
                slot_ids = futures[future]
                try:
                    if future.result():  # Conflict detected
                        conflicts.append(slot_ids)
                except Exception as e:
                    logger.error(f"Error checking conflict {slot_ids}: {e}")
        
        return {
            "total_pairs_checked": len(slot_pairs),
            "conflicts_found": len(conflicts),
            "conflict_pairs": conflicts
        }
    
    def optimize_with_solvers_parallel(
        self,
        problem_data: Dict,
        solver_fns: List[Tuple[str, callable]],
        timeout: float = 60.0
    ) -> Dict[str, Any]:
        """
        Run multiple solvers in parallel and return best solution
        Useful for comparing CSP solver vs greedy solver
        
        Args:
            problem_data: The scheduling problem
            solver_fns: List of (solver_name, solver_fn) tuples
            timeout: Max time for each solver
        
        Returns:
            Best solution found by any solver
        """
        self.logger.info(f"Running {len(solver_fns)} solvers in parallel")
        start_time = time.time()
        
        solutions = {}
        
        with ThreadPoolExecutor(max_workers=min(len(solver_fns), self.max_workers)) as executor:
            futures = {
                executor.submit(solver_fn, problem_data): solver_name
                for solver_name, solver_fn in solver_fns
            }
            
            for future in as_completed(futures, timeout=timeout):
                solver_name = futures[future]
                try:
                    solution = future.result(timeout=timeout)
                    solutions[solver_name] = {
                        "success": True,
                        "solution": solution,
                        "quality": self._evaluate_solution(solution)
                    }
                except Exception as e:
                    solutions[solver_name] = {
                        "success": False,
                        "error": str(e),
                        "quality": 0
                    }
        
        elapsed = time.time() - start_time
        
        # Return best solution
        best = max(
            [(k, v) for k, v in solutions.items() if v["success"]],
            key=lambda x: x[1]["quality"],
            default=(None, None)
        )
        
        return {
            "duration_seconds": elapsed,
            "solver_results": solutions,
            "best_solver": best[0],
            "best_solution": best[1] if best[1] else None,
            "all_solutions": solutions
        }
    
    @staticmethod
    def _evaluate_solution(solution: Dict) -> int:
        """Simple solution quality metric (higher is better)"""
        if not solution or "scheduled" not in solution:
            return 0
        return len(solution.get("scheduled", []))


class ParallelAvailabilityLoader:
    """Load availability data from multiple sources in parallel"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def load_all_sources(
        self,
        sources: Dict[str, callable]
    ) -> Dict[str, Any]:
        """
        Load data from multiple sources concurrently
        
        Args:
            sources: Dict of {source_name: loader_function}
        
        Returns:
            Dict of {source_name: loaded_data}
        """
        self.logger.info(f"Loading from {len(sources)} sources in parallel")
        start_time = time.time()
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(loader_fn): source_name
                for source_name, loader_fn in sources.items()
            }
            
            for future in as_completed(futures):
                source_name = futures[future]
                try:
                    data = future.result(timeout=30)
                    results[source_name] = {
                        "success": True,
                        "data": data
                    }
                    self.logger.info(f"Loaded from {source_name}")
                except Exception as e:
                    results[source_name] = {
                        "success": False,
                        "error": str(e)
                    }
                    self.logger.error(f"Failed to load from {source_name}: {e}")
        
        elapsed = time.time() - start_time
        
        return {
            "sources_loaded": sum(
                1 for r in results.values() if r.get("success")
            ),
            "sources_failed": sum(
                1 for r in results.values() if not r.get("success")
            ),
            "duration_seconds": elapsed,
            "results": results
        }
