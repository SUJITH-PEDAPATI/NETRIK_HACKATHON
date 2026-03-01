# phase6_escalation/engine/batch_processor.py

import logging
from phase6_escalation.engine.escalation_service import evaluate_with_context
from phase6_escalation.audit.audit_log import EscalationAuditLog
from utils.threading_manager import ConcurrentBatchProcessor, ProcessingMode

logger = logging.getLogger(__name__)

DEFAULT_LOG = "./output/escalation_audit.jsonl"


def _evaluate_and_record(
    query_dict: dict,
    audit: EscalationAuditLog
) -> dict:
    """
    Evaluate a single query and record to audit log
    This is the task function for concurrent processing
    """
    result = evaluate_with_context(
        query=query_dict.get("query", ""),
        employee_id=query_dict.get("employee_id"),
        employee_name=query_dict.get("employee_name"),
        source=query_dict.get("source", "pipeline"),
    )

    audit.record(
        result,
        employee_id=query_dict.get("employee_id"),
        source=query_dict.get("source", "pipeline")
    )

    return result


def screen_candidate_queries(
    queries: list[dict],
    log_path: str = DEFAULT_LOG,
    use_threading: bool = True,
    max_workers: int = 4,
) -> dict:
    """
    Screen candidate queries with optional parallel processing
    
    Args:
        queries: List of query dicts to process
        log_path: Path to audit log
        use_threading: Enable multi-threaded processing
        max_workers: Number of worker threads
    
    Returns:
        Dict with total, escalated, critical counts and results
    """
    
    audit = EscalationAuditLog(log_path)
    
    if not use_threading or len(queries) < 5:
        # Sequential processing for small batches
        logger.info(f"Processing {len(queries)} queries sequentially")
        results = []
        for q in queries:
            result = _evaluate_and_record(q, audit)
            results.append(result)
    else:
        # Parallel processing for large batches
        logger.info(f"Processing {len(queries)} queries with {max_workers} threads")
        processor = ConcurrentBatchProcessor(
            max_workers=max_workers,
            name="EscalationProcessor"
        )
        
        task_results = processor.process_batch(
            items=queries,
            task_fn=_evaluate_and_record,
            mode=ProcessingMode.THREADED,
            audit=audit
        )
        
        # Extract successful results
        results = [
            tr.result for tr in task_results
            if tr.success and tr.result is not None
        ]
        
        # Log statistics
        stats = processor.get_stats()
        logger.info(
            f"Batch processing complete - "
            f"Success rate: {stats['success_rate']:.1%}, "
            f"Time: {stats['total_time_seconds']:.2f}s"
        )

    escalated = [r for r in results if r["escalation"]]
    critical = [r for r in escalated if r.get("severity") == "critical"]

    return {
        "total": len(results),
        "escalated": len(escalated),
        "critical": critical,
        "results": results,
    }


def batch_process_large_dataset(
    queries: list[dict],
    log_path: str = DEFAULT_LOG,
    max_workers: int = 8,
    batch_size: int = 100,
) -> dict:
    """
    Process very large datasets with batching and multi-threading
    
    Args:
        queries: Large list of queries
        log_path: Audit log path
        max_workers: Number of threads
        batch_size: Items per batch
    
    Returns:
        Aggregated results across all batches
    """
    logger.info(
        f"Processing {len(queries)} queries in batches of {batch_size} "
        f"with {max_workers} threads"
    )
    
    all_results = []
    total_escalated = 0
    total_critical = 0
    
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} items)")
        
        batch_result = screen_candidate_queries(
            queries=batch,
            log_path=log_path,
            use_threading=True,
            max_workers=max_workers
        )
        
        all_results.extend(batch_result["results"])
        total_escalated += batch_result["escalated"]
        total_critical += len(batch_result["critical"])
    
    return {
        "total": len(all_results),
        "escalated": total_escalated,
        "critical": total_critical,
        "results": all_results,
    }