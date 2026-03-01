"""Export functionality for standardized JSON output."""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib


def export_results() -> Dict[str, Any]:
    """Generate standardized JSON export.
    
    Returns:
        Dictionary with all system outputs including:
        - rankings: Candidate rankings with scores
        - interviews: Scheduled interviews
        - schedule: Full scheduling calendar
        - leave_decisions: All leave requests and decisions
        - state_logs: State transition history
    """
    
    # Sample data - in production, this would pull from actual system state
    results = {
        "metadata": {
            "export_timestamp": datetime.now().isoformat(),
            "system_version": "1.0.0",
            "export_format": "standardized_json",
            "total_records": 0
        },
        
        "rankings": [
            {
                "rank": 1,
                "candidate_id": "CAND_001",
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "score": 92,
                "skills_match": 0.98,
                "experience_years": 5,
                "status": "qualified",
                "evaluation_date": "2026-03-01T10:00:00Z",
                "evaluator": "resume_screening_engine"
            },
            {
                "rank": 2,
                "candidate_id": "CAND_002",
                "name": "Bob Smith",
                "email": "bob@example.com",
                "score": 88,
                "skills_match": 0.85,
                "experience_years": 3,
                "status": "qualified",
                "evaluation_date": "2026-03-01T10:05:00Z",
                "evaluator": "resume_screening_engine"
            },
            {
                "rank": 3,
                "candidate_id": "CAND_003",
                "name": "Carol Davis",
                "email": "carol@example.com",
                "score": 85,
                "skills_match": 0.92,
                "experience_years": 6,
                "status": "review",
                "evaluation_date": "2026-03-01T10:10:00Z",
                "evaluator": "resume_screening_engine"
            }
        ],
        
        "interviews": [
            {
                "interview_id": "INT_001",
                "candidate_id": "CAND_001",
                "candidate_name": "Alice Johnson",
                "scheduled_date": "2026-03-05",
                "scheduled_time": "10:00",
                "duration_minutes": 60,
                "interviewer": "John Doe",
                "interviewer_id": "EMP_001",
                "status": "scheduled",
                "location": "Conference Room A",
                "meeting_link": "https://meet.example.com/int_001",
                "confirmation_status": "confirmed",
                "conflict_flags": []
            },
            {
                "interview_id": "INT_002",
                "candidate_id": "CAND_002",
                "candidate_name": "Bob Smith",
                "scheduled_date": "2026-03-05",
                "scheduled_time": "14:00",
                "duration_minutes": 45,
                "interviewer": "Jane Smith",
                "interviewer_id": "EMP_002",
                "status": "scheduled",
                "location": "Virtual",
                "meeting_link": "https://meet.example.com/int_002",
                "confirmation_status": "pending",
                "conflict_flags": []
            }
        ],
        
        "schedule": {
            "scheduling_algorithm": "constraint_satisfaction_problem",
            "optimization_metrics": {
                "total_conflicts": 0,
                "total_overlaps": 0,
                "utilization_rate": 0.75,
                "feasibility_score": 1.0
            },
            "calendar": [
                {
                    "date": "2026-03-05",
                    "day_of_week": "Wednesday",
                    "total_slots": 8,
                    "available_slots": 6,
                    "interviews_scheduled": 2,
                    "events": [
                        {
                            "time": "10:00-11:00",
                            "event_type": "interview",
                            "event_id": "INT_001",
                            "resource": "Conference Room A",
                            "participants": ["Alice Johnson", "John Doe"]
                        },
                        {
                            "time": "14:00-14:45",
                            "event_type": "interview",
                            "event_id": "INT_002",
                            "resource": "Virtual",
                            "participants": ["Bob Smith", "Jane Smith"]
                        }
                    ]
                }
            ]
        },
        
        "leave_decisions": [
            {
                "leave_id": "LEAVE_001",
                "employee_id": "EMP_001",
                "employee_name": "John Doe",
                "leave_type": "annual",
                "start_date": "2026-02-01",
                "end_date": "2026-02-05",
                "duration_days": 5,
                "status": "approved",
                "approval_date": "2026-01-30",
                "approver_id": "MGR_001",
                "approver_name": "Manager Name",
                "reason": "Vacation",
                "decision_logic": {
                    "policy_check": "passed",
                    "balance_check": "passed_with_balance_16",
                    "overlap_check": "no_conflicts",
                    "team_coverage_check": "passed",
                    "notice_period_check": "adequate",
                    "final_decision": "approved"
                }
            },
            {
                "leave_id": "LEAVE_002",
                "employee_id": "EMP_002",
                "employee_name": "Jane Smith",
                "leave_type": "sick",
                "start_date": "2026-01-20",
                "end_date": "2026-01-22",
                "duration_days": 3,
                "status": "approved",
                "approval_date": "2026-01-20",
                "approver_id": "system",
                "approver_name": "Auto Approval",
                "reason": "Medical Emergency",
                "decision_logic": {
                    "policy_check": "passed",
                    "balance_check": "passed",
                    "overlap_check": "no_conflicts",
                    "team_coverage_check": "N/A",
                    "notice_period_check": "waived_emergency",
                    "final_decision": "auto_approved"
                }
            }
        ],
        
        "state_logs": [
            {
                "log_id": "STATE_LOG_001",
                "candidate_id": "CAND_001",
                "candidate_name": "Alice Johnson",
                "timestamp": "2026-02-28T10:00:00Z",
                "from_state": "submitted",
                "to_state": "screening",
                "trigger": "auto_submit",
                "transition_metadata": {
                    "trigger_source": "system",
                    "processing_time_ms": 150,
                    "validation_passed": True
                }
            },
            {
                "log_id": "STATE_LOG_002",
                "candidate_id": "CAND_001",
                "candidate_name": "Alice Johnson",
                "timestamp": "2026-02-28T14:30:00Z",
                "from_state": "screening",
                "to_state": "qualified",
                "trigger": "resume_analysis_complete",
                "transition_metadata": {
                    "trigger_source": "interview_engine",
                    "score": 92,
                    "skills_match": 0.98,
                    "validation_passed": True
                }
            },
            {
                "log_id": "STATE_LOG_003",
                "candidate_id": "CAND_001",
                "candidate_name": "Alice Johnson",
                "timestamp": "2026-03-01T09:00:00Z",
                "from_state": "qualified",
                "to_state": "interview_scheduled",
                "trigger": "calendar_slot_found",
                "transition_metadata": {
                    "trigger_source": "scheduling_pipeline",
                    "interview_date": "2026-03-05",
                    "interview_time": "10:00",
                    "validation_passed": True
                }
            }
        ],
        
        "escalations": [
            {
                "escalation_id": "ESC_001",
                "category": "legal",
                "severity": "critical",
                "status": "open",
                "created_date": "2026-03-01",
                "description": "Employee reported potential legal threat",
                "confidence_score": 0.87,
                "detected_by": "rule_engine",
                "matching_rules": ["legal_threat_detection", "discrimination_keywords"],
                "assigned_to": "legal_team",
                "audit_trail": []
            }
        ]
    }
    
    # Update metadata
    results["metadata"]["total_records"] = (
        len(results["rankings"]) +
        len(results["interviews"]) +
        len(results["leave_decisions"]) +
        len(results["state_logs"]) +
        len(results["escalations"])
    )
    
    return results


def export_to_file(results: Dict[str, Any], filepath: str, format: str = "json") -> bool:
    """Export results to file.
    
    Args:
        results: Export results dictionary
        filepath: Output file path
        format: 'json', 'csv', or 'pdf'
        
    Returns:
        True if successful
    """
    try:
        if format == "json":
            with open(filepath, "w") as f:
                json.dump(results, f, indent=2, default=str)
        elif format == "csv":
            # Convert to CSV format (would need pandas)
            import pandas as pd
            data = []
            for key, records in results.items():
                if isinstance(records, list):
                    df = pd.DataFrame(records)
                    df.to_csv(f"{filepath}_{key}.csv", index=False)
        return True
    except Exception as e:
        print(f"Export failed: {str(e)}")
        return False


def generate_export_hash(results: Dict[str, Any]) -> str:
    """Generate SHA256 hash of export for verification.
    
    Args:
        results: Export results
        
    Returns:
        Hash string
    """
    json_str = json.dumps(results, sort_keys=True, default=str)
    return hashlib.sha256(json_str.encode()).hexdigest()


def validate_export_structure(results: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate export has required structure.
    
    Args:
        results: Export results
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    required_keys = ["rankings", "interviews", "schedule", "leave_decisions", "state_logs"]
    errors = []
    
    for key in required_keys:
        if key not in results:
            errors.append(f"Missing required key: {key}")
    
    return len(errors) == 0, errors
