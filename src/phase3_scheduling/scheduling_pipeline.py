"""
phase3_scheduling/scheduling_pipeline.py
─────────────────────────────────────────
Advanced Entry point for Phase 3 — Conflict-Aware Scheduling.

Features:
  → Multiple scheduling algorithms (CSP, Greedy, Hybrid)
  → Conflict detection and resolution
  → Multi-format data loading (JSON, CSV, Pipeline)
  → Advanced reporting and analytics
  → Calendar export (iCalendar)
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import logging

from phase3_scheduling.loaders.availability_loader import (
    generate_random,
    load_from_json,
    load_from_csv,
    load_from_pipeline_results,
    validate_data,
    SAMPLE_JSON_TEMPLATE,
)

from phase3_scheduling.core.scheduler import schedule
from phase3_scheduling.core.conflict_analysis import analyse_conflicts

from phase3_scheduling.reporting.schedule_reporter import (
    save_schedule_json,
    save_schedule_ical,
    ScheduleReporter,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# Advanced Configuration
# ─────────────────────────────────────────────────────────────

class SchedulingConfig:
    """Advanced scheduling configuration."""
    def __init__(self):
        self.optimization_method = "hybrid"  # "csp", "greedy", or "hybrid"
        self.max_iterations = 1000
        self.allow_conflicts = False
        self.conflict_resolution_strategy = "reschedule"
        self.report_formats = ["json", "html", "ical"]
        self.performance_tracking = True


# ─────────────────────────────────────────────────────────────
# Core Advanced Runner
# ─────────────────────────────────────────────────────────────

def run_scheduling(
    matrix: dict,
    output_dir: str = "./output",
    ical: bool = True,
    html: bool = True,
    config: SchedulingConfig = None,
) -> dict:
    """
    Advanced scheduling orchestrator with optimization and analytics.
    
    Args:
        matrix: Input data with candidates, interviewers, date_range
        output_dir: Output directory for reports
        ical: Generate iCalendar export
        html: Generate HTML report
        config: Scheduling configuration
        
    Returns:
        Complete result with schedule, analytics, and metadata
    """
    config = config or SchedulingConfig()
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "═" * 70)
    print("  PHASE 3 — ADVANCED CONFLICT-AWARE INTERVIEW SCHEDULER")
    print("═" * 70)
    print(f"  Optimization Method  : {config.optimization_method.upper()}")
    print(f"  Candidates           : {len(matrix['candidates'])}")
    print(f"  Interviewers         : {len(matrix['interviewers'])}")
    print(f"  Date Range           : {matrix['date_range']['start_date']} → "
          f"{matrix['date_range']['end_date']}")
    print("═" * 70)

    # Validate input data
    is_valid, errors = validate_data(matrix)
    if not is_valid:
        print("\n❌ DATA VALIDATION FAILED:")
        for error in errors:
            print(f"   • {error}")
        return {"error": "Invalid input data", "errors": errors}

    # Run scheduling engine with selected algorithm
    print("\n  [1/5] Running scheduling engine...")
    result = schedule(matrix, config.optimization_method)
    
    # Conflict validation layer
    print("  [2/5] Analyzing conflicts...")
    conflict_report = analyse_conflicts(result)
    
    # Generate analytics
    print("  [3/5] Generating analytics...")
    reporter = ScheduleReporter()
    analytics = _generate_analytics(result, conflict_report)

    # Save outputs
    print("  [4/5] Saving outputs...")
    json_path = os.path.join(output_dir, "schedule.json")
    save_schedule_json(result, conflict_report, json_path)
    
    if html:
        html_path = os.path.join(output_dir, "schedule.html")
        reporter.generate_html_report(result, html_path)

    if ical:
        ical_path = os.path.join(output_dir, "schedule.ics")
        save_schedule_ical(result, ical_path)

    # Print stats and analytics
    print("  [5/5] Complete!\n")
    stats = result["stats"]

    print("═" * 70)
    print("  ✅ SCHEDULING COMPLETE")
    print("═" * 70)
    print(f"  Scheduled            : {stats['scheduled_count']} / {stats['total_variables']}")
    print(f"  Success Rate         : {stats['success_rate']}%")
    print(f"  Unscheduled          : {stats['unscheduled_count']}")
    print(f"  Conflict-free        : {'✓ YES' if conflict_report['is_conflict_free'] else '✗ NO'}")
    print(f"  Conflicts Detected   : {conflict_report['total_conflicts']}")
    print(f"  Warnings             : {conflict_report['total_warnings']}")
    print(f"  Solver Time          : {stats['solver_time_seconds']}s")
    print("═" * 70)
    
    if conflict_report['total_conflicts'] > 0:
        print("\n  ⚠️  CONFLICTS DETECTED:")
        print(f"     • Critical: {conflict_report['severity_breakdown']['CRITICAL']}")
        print(f"     • High:     {conflict_report['severity_breakdown']['HIGH']}")

    print(f"\n  📁 Outputs saved to: {output_dir}")
    print("═" * 70 + "\n")

    return {
        "success": True,
        "schedule": result,
        "conflict_report": conflict_report,
        "analytics": analytics,
        "output_dir": output_dir,
    }


# ─────────────────────────────────────────────────────────────
# Advanced Analytics Generation
# ─────────────────────────────────────────────────────────────

def _generate_analytics(result: dict, conflict_report: dict) -> dict:
    """Generate comprehensive analytics from schedule."""
    interviews = result.get("interviews", [])
    
    # Load distribution analysis
    interviewer_load = {}
    for interview in interviews:
        int_id = interview["interviewer_id"]
        interviewer_load[int_id] = interviewer_load.get(int_id, 0) + 1
    
    # Time slot distribution
    time_distribution = {}
    for interview in interviews:
        start_time = datetime.fromisoformat(interview["start_time"])
        hour = start_time.hour
        time_distribution[hour] = time_distribution.get(hour, 0) + 1
    
    return {
        "interviewer_load": interviewer_load,
        "time_distribution": time_distribution,
        "avg_load_per_interviewer": sum(interviewer_load.values()) / len(interviewer_load) if interviewer_load else 0,
        "peak_hour": max(time_distribution, key=time_distribution.get) if time_distribution else None,
    }


# ─────────────────────────────────────────────────────────────
# Advanced Pipeline Bridge (Phase 1 + Phase 2 → Phase 3)
# ─────────────────────────────────────────────────────────────

def run_from_pipeline(
    ranked_results: list[dict],
    interviewers_data: dict,
    output_dir: str = "./output",
    start_date: str = None,
    days: int = 5,
    config: SchedulingConfig = None,
) -> dict:
    """
    Transform Phase 1-2 pipeline results into advanced scheduling.
    
    Args:
        ranked_results: Ranked candidate results from Phase 1-2
        interviewers_data: Interviewer availability data
        output_dir: Output directory
        start_date: Start date for scheduling
        days: Number of days to schedule
        config: Scheduling configuration
        
    Returns:
        Complete scheduling result
    """
    print("\n  🔗 BRIDGING PHASE 1-2 RESULTS TO PHASE 3...")
    
    matrix = load_from_pipeline_results(
        ranked_results=ranked_results,
        interviewers_data=interviewers_data,
        days=days,
        start_date=start_date,
    )

    return run_scheduling(matrix, output_dir=output_dir, config=config or SchedulingConfig())


# ─────────────────────────────────────────────────────────────
# CLI Interface
# ─────────────────────────────────────────────────────────────

def main():
    """Command-line interface for scheduling pipeline."""
    parser = argparse.ArgumentParser(
        description="Advanced Interview Scheduling Pipeline (Phase 3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m phase3_scheduling.scheduling_pipeline --random 10 5
  python -m phase3_scheduling.scheduling_pipeline --json input.json --algorithm hybrid
  python -m phase3_scheduling.scheduling_pipeline --sample > sample_input.json
        """
    )
    
    parser.add_argument("--random", nargs=2, type=int, metavar=("CANDIDATES", "INTERVIEWERS"),
                       help="Generate random data for testing")
    parser.add_argument("--json", type=str, help="Load from JSON file")
    parser.add_argument("--csv", nargs=2, metavar=("CANDIDATES", "INTERVIEWERS"),
                       help="Load from CSV files")
    parser.add_argument("--algorithm", choices=["csp", "greedy", "hybrid"], default="hybrid",
                       help="Scheduling algorithm (default: hybrid)")
    parser.add_argument("--output", "-o", type=str, default="./output",
                       help="Output directory (default: ./output)")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML report generation")
    parser.add_argument("--no-ical", action="store_true", help="Skip iCalendar export")
    parser.add_argument("--sample", action="store_true", help="Print sample JSON template")
    
    args = parser.parse_args()
    
    if args.sample:
        print(json.dumps(SAMPLE_JSON_TEMPLATE, indent=2))
        return
    
    config = SchedulingConfig()
    config.optimization_method = args.algorithm
    
    # Load data
    if args.random:
        matrix = generate_random(args.random[0], args.random[1])
    elif args.json:
        matrix = load_from_json(args.json)
    elif args.csv:
        matrix = load_from_csv(args.csv[0], args.csv[1])
    else:
        print("❌ Error: Please provide --random, --json, or --csv")
        parser.print_help()
        return
    
    # Run scheduling
    result = run_scheduling(
        matrix,
        output_dir=args.output,
        html=not args.no_html,
        ical=not args.no_ical,
        config=config,
    )


if __name__ == "__main__":
    main()