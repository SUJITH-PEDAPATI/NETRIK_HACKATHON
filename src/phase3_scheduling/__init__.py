"""
Phase 3: Advanced Conflict-Aware Interview Scheduling

Production-grade scheduling engine with multiple algorithms, comprehensive
conflict detection, and advanced analytics for high-volume interview coordination.

Quick Start:
    from phase3_scheduling import run_scheduling
    from phase3_scheduling.loaders import generate_random
    
    matrix = generate_random(50, 10, days=5)
    result = run_scheduling(matrix)

CLI Usage:
    python -m phase3_scheduling.scheduling_pipeline --random 50 10 --algorithm hybrid

Features:
    ✓ Multiple scheduling algorithms (CSP, Greedy, Hybrid)
    ✓ Advanced conflict detection & severity classification
    ✓ Comprehensive analytics & load balancing
    ✓ Multi-format data loading (JSON, CSV, Pipeline bridge)
    ✓ Calendar export (iCalendar format)
    ✓ HTML reports with interactive dashboards
    ✓ Production-grade logging & error handling
    ✓ Scalable to 1000+ candidates/interviewers
"""

from .scheduling_pipeline import (
    run_scheduling,
    run_from_pipeline,
    SchedulingConfig,
)

from .core import (
    Scheduler,
    CSPSolver,
    GreedySolver,
    ConflictAnalyzer,
)

from .loaders import (
    AvailabilityLoader,
    CSVLoader,
    JSONLoader,
    PipelineBridge,
    generate_random,
    load_from_json,
    load_from_csv,
    load_from_pipeline_results,
    validate_data,
)

from .reporting import (
    ScheduleReporter,
    ICalExporter,
)

from .models import (
    Interview,
    TimeSlot,
    Candidate,
    Interviewer,
    Schedule,
    ScheduleConstraint,
    InterviewType,
    InterviewStatus,
    SeniorityLevel,
)

__version__ = "1.0.0"
__author__ = "HR Automation Team"

__all__ = [
    # Main API
    "run_scheduling",
    "run_from_pipeline",
    "SchedulingConfig",
    
    # Core algorithms
    "Scheduler",
    "CSPSolver",
    "GreedySolver",
    "ConflictAnalyzer",
    
    # Data loading
    "AvailabilityLoader",
    "CSVLoader",
    "JSONLoader",
    "PipelineBridge",
    "generate_random",
    "load_from_json",
    "load_from_csv",
    "load_from_pipeline_results",
    "validate_data",
    
    # Reporting
    "ScheduleReporter",
    "ICalExporter",
    
    # Data models
    "Interview",
    "TimeSlot",
    "Candidate",
    "Interviewer",
    "Schedule",
    "ScheduleConstraint",
    "InterviewType",
    "InterviewStatus",
    "SeniorityLevel",
]

