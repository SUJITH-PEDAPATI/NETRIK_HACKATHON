"""
Parallel Resume Processing & Candidate Evaluation
High-performance batch processing for resume extraction and evaluation
"""

import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Callable
import time

logger = logging.getLogger(__name__)


class ParallelResumeProcessor:
    """
    Process multiple resumes in parallel
    Extraction, parsing, and initial screening
    """
    
    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def process_resumes(
        self,
        resume_files: List[Dict[str, Any]],
        extractor_fn: Callable,
        parser_fn: Callable,
        normalize_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Extract text and parse multiple resumes in parallel
        
        Args:
            resume_files: List of resume file dicts
            extractor_fn: Function to extract text from file
            parser_fn: Function to parse extracted text
            normalize_fn: Optional function to normalize parsed data
        
        Returns:
            Dict with results, success rate, timing
        """
        self.logger.info(f"Processing {len(resume_files)} resumes with {self.max_workers} threads")
        start_time = time.time()
        
        results = []
        failed = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="ResumeProcessor") as executor:
            futures = {
                executor.submit(
                    self._process_single_resume,
                    resume,
                    extractor_fn,
                    parser_fn,
                    normalize_fn
                ): resume.get("file_id", resume.get("filename"))
                for resume in resume_files
            }
            
            for future in as_completed(futures):
                resume_id = futures[future]
                try:
                    result = future.result(timeout=60)
                    if result["success"]:
                        results.append(result)
                    else:
                        failed.append(result)
                except Exception as e:
                    failed.append({
                        "resume_id": resume_id,
                        "success": False,
                        "error": str(e)
                    })
        
        elapsed = time.time() - start_time
        
        self.logger.info(
            f"Resume processing complete: {len(results)} success, "
            f"{len(failed)} failed in {elapsed:.2f}s"
        )
        
        return {
            "total": len(resume_files),
            "success": len(results),
            "failed": len(failed),
            "success_rate": len(results) / len(resume_files) if resume_files else 0,
            "results": results,
            "failures": failed,
            "duration_seconds": elapsed
        }
    
    @staticmethod
    def _process_single_resume(
        resume: Dict[str, Any],
        extractor_fn: Callable,
        parser_fn: Callable,
        normalize_fn: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Process a single resume"""
        try:
            # Extract text
            text = extractor_fn(resume)
            
            # Parse structured data
            parsed = parser_fn(text)
            
            # Normalize if provided
            if normalize_fn:
                parsed = normalize_fn(parsed)
            
            return {
                "resume_id": resume.get("file_id", resume.get("filename")),
                "success": True,
                "extracted_text": text[:500],  # Preview
                "parsed_data": parsed
            }
        except Exception as e:
            return {
                "resume_id": resume.get("file_id", resume.get("filename")),
                "success": False,
                "error": str(e)
            }


class ParallelCandidateEvaluator:
    """
    Evaluate multiple candidates in parallel
    Question generation, assessment, scoring
    """
    
    def __init__(self, max_workers: int = 6):
        self.max_workers = max_workers
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def evaluate_candidates(
        self,
        candidates: List[Dict[str, Any]],
        question_generator_fn: Callable,
        assessor_fn: Callable,
        evaluator_fn: Callable,
        use_processes: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluate multiple candidates in parallel
        
        Args:
            candidates: List of candidate dicts
            question_generator_fn: Generate questions for candidate
            assessor_fn: Assess answers
            evaluator_fn: Overall evaluation
            use_processes: Use ProcessPoolExecutor for CPU-bound work
        
        Returns:
            Evaluation results with ratings and scores
        """
        self.logger.info(
            f"Evaluating {len(candidates)} candidates "
            f"with {self.max_workers} {'processes' if use_processes else 'threads'}"
        )
        start_time = time.time()
        
        results = []
        failed = []
        
        executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
        
        with executor_class(max_workers=self.max_workers, thread_name_prefix="Evaluator") as executor:
            futures = {
                executor.submit(
                    self._evaluate_single_candidate,
                    candidate,
                    question_generator_fn,
                    assessor_fn,
                    evaluator_fn
                ): candidate.get("candidate_id", candidate.get("name"))
                for candidate in candidates
            }
            
            for future in as_completed(futures):
                candidate_id = futures[future]
                try:
                    result = future.result(timeout=120)
                    if result["success"]:
                        results.append(result)
                    else:
                        failed.append(result)
                except Exception as e:
                    failed.append({
                        "candidate_id": candidate_id,
                        "success": False,
                        "error": str(e)
                    })
        
        elapsed = time.time() - start_time
        
        # Sort by score (descending)
        results.sort(
            key=lambda x: x.get("overall_score", 0),
            reverse=True
        )
        
        self.logger.info(
            f"Evaluation complete: {len(results)} success, "
            f"{len(failed)} failed in {elapsed:.2f}s"
        )
        
        return {
            "total": len(candidates),
            "success": len(results),
            "failed": len(failed),
            "success_rate": len(results) / len(candidates) if candidates else 0,
            "ranked_results": results,
            "failures": failed,
            "duration_seconds": elapsed,
            "average_score": (
                sum(r.get("overall_score", 0) for r in results) / len(results)
                if results else 0
            )
        }
    
    @staticmethod
    def _evaluate_single_candidate(
        candidate: Dict[str, Any],
        question_generator_fn: Callable,
        assessor_fn: Callable,
        evaluator_fn: Callable
    ) -> Dict[str, Any]:
        """Evaluate a single candidate"""
        try:
            # Generate questions
            questions = question_generator_fn(candidate)
            
            # Get answers and assess
            answers = candidate.get("answers", [])
            assessments = [assessor_fn(q, a) for q, a in zip(questions, answers)]
            
            # Overall evaluation
            evaluation = evaluator_fn(candidate, questions, assessments)
            
            return {
                "candidate_id": candidate.get("candidate_id", candidate.get("name")),
                "success": True,
                "overall_score": evaluation.get("overall_score", 0),
                "rating": evaluation.get("rating"),
                "skill_assessments": evaluation.get("skill_assessments", {}),
                "recommendation": evaluation.get("recommendation"),
                "evaluation": evaluation
            }
        except Exception as e:
            return {
                "candidate_id": candidate.get("candidate_id", candidate.get("name")),
                "success": False,
                "error": str(e)
            }
    
    def adaptive_batch_evaluation(
        self,
        candidates: List[Dict[str, Any]],
        question_generator_fn: Callable,
        assessor_fn: Callable,
        evaluator_fn: Callable,
        batch_size: int = 10,
        performance_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Smart batching: process high-potential candidates with more depth
        
        Args:
            candidates: All candidates
            batch_size: Initial batch size
            performance_threshold: Score threshold for deeper evaluation
        
        Returns:
            Stratified evaluation results
        """
        self.logger.info(
            f"Adaptive evaluation of {len(candidates)} candidates "
            f"with {batch_size} item batches"
        )
        
        all_results = []
        batch_num = 0
        
        # First pass: quick evaluation
        for i in range(0, len(candidates), batch_size):
            batch = candidates[i:i + batch_size]
            batch_num += 1
            self.logger.info(f"Batch {batch_num}: Quick evaluation of {len(batch)} candidates")
            
            batch_results = self.evaluate_candidates(
                candidates=batch,
                question_generator_fn=question_generator_fn,
                assessor_fn=assessor_fn,
                evaluator_fn=evaluator_fn,
                use_processes=False
            )
            
            all_results.extend(batch_results["ranked_results"])
        
        # Second pass: Deep dive on high-performers
        high_performers = [
            r for r in all_results
            if r.get("overall_score", 0) >= performance_threshold
        ]
        
        if high_performers:
            self.logger.info(f"Deep evaluation of {len(high_performers)} high-performers")
            
            deep_results = self.evaluate_candidates(
                candidates=[
                    {**r, "detailed_assessment": True}
                    for r in high_performers
                ],
                question_generator_fn=question_generator_fn,
                assessor_fn=assessor_fn,
                evaluator_fn=evaluator_fn,
                use_processes=False
            )
            
            # Merge deep results
            all_results = [
                next((dr for dr in deep_results["ranked_results"] 
                      if dr.get("candidate_id") == r.get("candidate_id")), r)
                for r in all_results
            ]
        
        return {
            "total": len(candidates),
            "high_performers": len(high_performers),
            "results": sorted(
                all_results,
                key=lambda x: x.get("overall_score", 0),
                reverse=True
            )
        }


class ParallelPersistenceHandler:
    """
    Write/read multiple records to storage in parallel
    Prevents I/O bottleneck
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def save_records_parallel(
        self,
        records: List[Dict[str, Any]],
        save_fn: Callable
    ) -> Dict[str, Any]:
        """
        Save multiple records in parallel
        
        Args:
            records: List of records to save
            save_fn: Function to save single record
        
        Returns:
            Success count and timing
        """
        self.logger.info(f"Saving {len(records)} records in parallel")
        start_time = time.time()
        
        saved = 0
        failed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="PersistenceWriter") as executor:
            futures = {
                executor.submit(save_fn, record): record.get("id")
                for record in records
            }
            
            for future in as_completed(futures):
                try:
                    future.result(timeout=10)
                    saved += 1
                except Exception as e:
                    failed += 1
                    self.logger.error(f"Error saving record: {e}")
        
        elapsed = time.time() - start_time
        
        self.logger.info(
            f"Save complete: {saved} success, {failed} failed in {elapsed:.2f}s"
        )
        
        return {
            "total": len(records),
            "saved": saved,
            "failed": failed,
            "duration_seconds": elapsed
        }
    
    def load_records_parallel(
        self,
        record_ids: List[str],
        load_fn: Callable
    ) -> Dict[str, Any]:
        """Load multiple records in parallel"""
        self.logger.info(f"Loading {len(record_ids)} records in parallel")
        start_time = time.time()
        
        records = {}
        failed = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="PersistenceReader") as executor:
            futures = {
                executor.submit(load_fn, rid): rid
                for rid in record_ids
            }
            
            for future in as_completed(futures):
                rid = futures[future]
                try:
                    record = future.result(timeout=10)
                    records[rid] = record
                except Exception as e:
                    failed.append(rid)
                    self.logger.error(f"Error loading record {rid}: {e}")
        
        elapsed = time.time() - start_time
        
        return {
            "total": len(record_ids),
            "loaded": len(records),
            "failed": len(failed),
            "records": records,
            "duration_seconds": elapsed
        }
