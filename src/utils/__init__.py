"""Utilities module initialization."""

from .export_manager import export_results, export_to_file, validate_export_structure
from .logging_system import get_logger, log_event, EventAuditTrail
from .explanation_engine import get_decision_explanation, generate_decision_report
from .metrics_dashboard import get_system_metrics, MetricsDashboard
from .threading_manager import (
    ConcurrentBatchProcessor,
    AsyncAuditLogger,
    WorkerPool,
    ThreadSafeLogger,
    ProcessingMode,
    parallel_map,
    run_async,
    run_in_thread_pool
)

__all__ = [
    "export_results",
    "export_to_file",
    "validate_export_structure",
    "get_logger",
    "log_event",
    "EventAuditTrail",
    "get_decision_explanation",
    "generate_decision_report",
    "get_system_metrics",
    "MetricsDashboard",
    # Threading & Concurrency
    "ConcurrentBatchProcessor",
    "AsyncAuditLogger",
    "WorkerPool",
    "ThreadSafeLogger",
    "ProcessingMode",
    "parallel_map",
    "run_async",
    "run_in_thread_pool"
]
