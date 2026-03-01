"""
Integration Examples: Using Multithreading in the Pipeline
Add these to your main pipeline.py
"""

# ============================================================================
# EXAMPLE 1: Update Phase 1 (Interview Engine) for Parallel Evaluation
# ============================================================================

def evaluate_candidates_parallel(candidates_data, config):
    """
    Updated candidate evaluation using parallel processing
    Replaces the sequential evaluation loop
    """
    from interview_engine.parallel_evaluator import (
        ParallelResumeProcessor,
        ParallelCandidateEvaluator
    )
    from interview_engine.question_bank.evaluator import Evaluator
    from interview_engine.question_bank.assessor import Assessor
    
    # Configure threading
    max_workers = config.get("evaluation_workers", 6)
    
    # Step 1: Extract resumes in parallel
    resume_processor = ParallelResumeProcessor(max_workers=max_workers + 2)
    resume_results = resume_processor.process_resumes(
        resume_files=candidates_data,
        extractor_fn=lambda r: extract_text_from_resume(r),
        parser_fn=lambda t: parse_resume_text(t)
    )
    
    print(f"✓ Processed {resume_results['success']} resumes in {resume_results['duration_seconds']:.1f}s")
    
    # Step 2: Evaluate candidates in parallel
    evaluator = ParallelCandidateEvaluator(max_workers=max_workers)
    eval_results = evaluator.evaluate_candidates(
        candidates=resume_results['results'],
        question_generator_fn=lambda c: generate_adaptive_questions(c),
        assessor_fn=lambda q, a: assess_answer(q, a),
        evaluator_fn=lambda c, qs, as_: evaluate_overall(c, qs, as_)
    )
    
    print(f"✓ Evaluated {eval_results['success']} candidates in {eval_results['duration_seconds']:.1f}s")
    print(f"  Average score: {eval_results['average_score']:.1f}/100")
    
    return eval_results['ranked_results']


# ============================================================================
# EXAMPLE 2: Update Phase 3 (Scheduling) for Parallel Processing
# ============================================================================

def schedule_interviews_parallel(interview_requests, availability_data, config):
    """
    Updated interview scheduling using parallel CSP solver
    """
    from phase3_scheduling.concurrent_scheduler import (
        ConcurrentScheduler,
        SchedulingParams,
        ParallelAvailabilityLoader
    )
    
    # Step 1: Load availability data in parallel from multiple sources
    loader = ParallelAvailabilityLoader(max_workers=4)
    availability = loader.load_all_sources({
        "google_calendar": lambda: fetch_google_calendar(),
        "exchange_calendar": lambda: fetch_exchange_calendar(),
        "local_db": lambda: load_local_availability(),
        "external_system": lambda: fetch_external_availability()
    })
    
    print(f"✓ Loaded availability from {availability['sources_loaded']} sources "
          f"in {availability['duration_seconds']:.1f}s")
    
    # Step 2: Convert requests to scheduling params
    params = [
        SchedulingParams(
            interviewer_id=req['interviewer_id'],
            candidate_id=req['candidate_id'],
            preferred_slots=req['preferred_slots'],
            constraints=req.get('constraints', {}),
            duration_minutes=req.get('duration', 60)
        )
        for req in interview_requests
    ]
    
    # Step 3: Schedule in parallel
    scheduler = ConcurrentScheduler(max_workers=config.get("scheduling_workers", 8))
    schedule_result = scheduler.schedule_batch(
        scheduling_params=params,
        conflict_checker_fn=lambda iid, slot: check_conflict(iid, slot, availability),
        scheduler_fn=lambda cid, slots, cons: find_best_slot(cid, slots, cons)
    )
    
    print(f"✓ Scheduled {schedule_result['scheduled']} interviews "
          f"in {schedule_result['duration_seconds']:.1f}s")
    
    return schedule_result['results']


# ============================================================================
# EXAMPLE 3: Update Phase 4 (Leave) with Async Logging
# ============================================================================

def process_leave_requests_with_async_logging(leave_requests, policy_engine, config):
    """
    Process leave requests with asynchronous audit logging
    """
    from utils.threading_manager import AsyncAuditLogger
    from phase4_leave.engine.leave_policy_engine import evaluate_leave_request
    
    # Create async logger (non-blocking)
    audit_logger = AsyncAuditLogger("LeaveAuditLog")
    
    results = []
    
    for req in leave_requests:
        # Process leave request
        decision = evaluate_leave_request(req, policy_engine)
        results.append(decision)
        
        # Log asynchronously (returns immediately, doesn't block main thread)
        audit_logger.log_event(
            event_type="leave_decision",
            data={
                "employee_id": req['employee_id'],
                "decision": decision['status'],
                "reason": decision.get('reason'),
                "timestamp": time.time()
            }
        )
    
    # Optionally wait for all logs to complete
    audit_logger.flush()
    audit_logger.shutdown()
    
    print(f"✓ Processed {len(results)} leave requests with async logging")
    return results


# ============================================================================
# EXAMPLE 4: Update Phase 6 (Escalation) for Parallel Detection
# ============================================================================

def detect_escalations_parallel(escalation_cases, config):
    """
    Detect escalations in high volume using parallel processing
    """
    from phase6_escalation.engine.batch_processor import (
        screen_candidate_queries,
        batch_process_large_dataset
    )
    
    max_workers = config.get("escalation_workers", 8)
    
    if len(escalation_cases) < 100:
        # Small batch: use threading
        results = screen_candidate_queries(
            queries=escalation_cases,
            use_threading=True,
            max_workers=max_workers
        )
        processing_time = 0  # Not tracked in this version
    else:
        # Large batch: use smart batching
        results = batch_process_large_dataset(
            queries=escalation_cases,
            max_workers=max_workers,
            batch_size=100
        )
        processing_time = 0  # Not tracked
    
    print(f"✓ Screened {results['total']} escalation cases")
    print(f"  Escalated: {results['escalated']}")
    print(f"  Critical: {len(results['critical'])}")
    
    return results


# ============================================================================
# EXAMPLE 5: Unified Pipeline with All Optimizations
# ============================================================================

def run_optimized_pipeline(config):
    """
    Complete HR automation pipeline with all threading optimizations
    """
    import json
    from utils.logging_system import get_logger
    from utils.export_manager import export_results
    
    logger = get_logger("OptimizedPipeline")
    logger.info("Starting optimized HR automation pipeline with multithreading")
    
    # ========== Phase 1: Resume Screening ==========
    logger.info("Phase 1: Resume extraction and evaluation")
    
    resume_data = load_resume_data(config)  # Your data loading function
    candidates_ranked = evaluate_candidates_parallel(resume_data, config)
    
    logger.info(f"Phase 1 complete: {len(candidates_ranked)} candidates ranked")
    
    # ========== Phase 3: Interview Scheduling ==========
    logger.info("Phase 3: Parallel interview scheduling")
    
    interview_reqs = prepare_scheduling_requests(candidates_ranked)
    availability = fetch_all_availability(config)
    scheduled_interviews = schedule_interviews_parallel(
        interview_reqs,
        availability,
        config
    )
    
    logger.info(f"Phase 3 complete: {len(scheduled_interviews)} interviews scheduled")
    
    # ========== Phase 4: Leave Management ==========
    logger.info("Phase 4: Leave request processing")
    
    leave_requests = load_leave_requests(config)
    leave_engine = initialize_leave_engine(config)
    leave_decisions = process_leave_requests_with_async_logging(
        leave_requests,
        leave_engine,
        config
    )
    
    logger.info(f"Phase 4 complete: {len(leave_decisions)} leave requests processed")
    
    # ========== Phase 6: Escalation Detection ==========
    logger.info("Phase 6: Parallel escalation detection")
    
    escalation_cases = prepare_escalation_cases(candidates_ranked, leave_decisions)
    escalation_results = detect_escalations_parallel(escalation_cases, config)
    
    logger.info(f"Phase 6 complete: {escalation_results['escalated']} escalations detected")
    
    # ========== Export Results ==========
    logger.info("Exporting results")
    
    export_data = export_results(
        rankings=candidates_ranked,
        interviews=scheduled_interviews,
        leave_decisions=leave_decisions,
        escalations=escalation_results['results']
    )
    
    output_file = config.get("output_file", "results.json")
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    logger.info(f"✓ Pipeline complete! Results exported to {output_file}")
    
    return export_data


# ============================================================================
# EXAMPLE 6: Batch Processing Large Datasets
# ============================================================================

def process_large_dataset_with_batching(input_file, config):
    """
    Process very large datasets (10,000+ items) with intelligent batching
    """
    from utils.threading_manager import ConcurrentBatchProcessor, ProcessingMode
    import json
    
    # Load data
    with open(input_file, 'r') as f:
        all_items = json.load(f)
    
    # Configure processor
    processor = ConcurrentBatchProcessor(
        max_workers=config.get("batch_workers", 8),
        batch_size=config.get("batch_size", 100),
        enable_monitoring=True
    )
    
    # Process in batches
    all_results = []
    batch_count = 0
    
    for i in range(0, len(all_items), config.get("batch_size", 100)):
        batch = all_items[i:i + config.get("batch_size", 100)]
        batch_count += 1
        
        print(f"Processing batch {batch_count} ({len(batch)} items)...")
        
        results = processor.process_batch(
            items=batch,
            task_fn=process_single_item,
            mode=ProcessingMode.THREADED,
            config=config
        )
        
        all_results.extend([r for r in results if r.success])
    
    # Print statistics
    stats = processor.get_stats()
    print(f"""
    Processing Complete!
    - Total items: {len(all_items)}
    - Successfully processed: {len(all_results)}
    - Total time: {stats['total_time_seconds']:.2f}s
    - Efficiency ratio: {stats['efficiency_ratio']:.1%}
    - Success rate: {stats['success_rate']:.1%}
    """)
    
    return all_results


# ============================================================================
# Configuration Example
# ============================================================================

# Add this to your config.py:
OPTIMIZED_CONFIG = {
    # Multithreading settings
    "enable_threading": True,
    
    # Per-phase worker counts (tune based on your CPU cores)
    "evaluation_workers": 6,        # Resume & candidate evaluation
    "scheduling_workers": 8,        # Interview scheduling
    "escalation_workers": 8,        # Escalation detection
    "persistence_workers": 4,       # Database I/O
    "batch_workers": 8,             # General batch processing
    
    # Batch sizes
    "batch_size": 50,               # Items per batch
    "escalation_batch_size": 100,   # Escalation batch size
    
    # Timeouts
    "task_timeout": 30.0,           # Seconds per task
    "batch_timeout": 300.0,         # Seconds per batch
    
    # Logging
    "enable_async_logging": True,   # Non-blocking audit logs
    
    # Output
    "output_file": "results.json",
}


# ============================================================================
# Performance Measurement Example
# ============================================================================

def measure_pipeline_performance(config):
    """
    Compare sequential vs parallel pipeline performance
    """
    import time
    
    test_config_sequential = {**config, "enable_threading": False}
    test_config_parallel = {**config, "enable_threading": True}
    
    # Run sequential
    print("Running sequential pipeline...")
    start = time.time()
    seq_results = run_optimized_pipeline(test_config_sequential)
    seq_time = time.time() - start
    
    # Run parallel
    print("Running parallel pipeline...")
    start = time.time()
    par_results = run_optimized_pipeline(test_config_parallel)
    par_time = time.time() - start
    
    # Compare
    speedup = seq_time / par_time
    
    print(f"""
    Performance Comparison:
    - Sequential: {seq_time:.2f}s
    - Parallel: {par_time:.2f}s
    - Speedup: {speedup:.1f}x
    - Improvement: {(1 - par_time/seq_time) * 100:.0f}%
    """)
    
    return speedup


if __name__ == "__main__":
    # Example usage
    config = OPTIMIZED_CONFIG
    
    # Run optimized pipeline
    print("=" * 70)
    print("HR AUTOMATION PIPELINE - MULTITHREADED VERSION")
    print("=" * 70)
    
    results = run_optimized_pipeline(config)
    
    print("\nPipeline completed successfully!")
    print(f"Processed {len(results)} total records.")
