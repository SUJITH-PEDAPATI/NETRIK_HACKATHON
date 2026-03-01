"""
phase3_scheduling/reporting/schedule_reporter.py
─────────────────────────────────────────────────
Advanced schedule reporting and analytics.
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def save_schedule_json(result: Dict, conflict_report: Dict, output_path: str) -> None:
    """Save schedule to JSON file."""
    data = {
        "timestamp": datetime.now().isoformat(),
        "schedule": result,
        "conflict_analysis": conflict_report,
    }
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    logger.info(f"Schedule saved to {output_path}")


class ScheduleReporter:
    """Advanced schedule reporting and analytics."""
    
    def __init__(self):
        """Initialize schedule reporter."""
        logger.info("Initialized ScheduleReporter")
    
    def generate_summary(self, schedule: Dict) -> str:
        """
        Generate summary report.
        
        Args:
            schedule: Schedule dictionary
            
        Returns:
            Summary text
        """
        interviews = schedule.get("interviews", [])
        stats = schedule.get("stats", {})
        
        summary = f"""
SCHEDULE SUMMARY
{'='*60}
Total Interviews Scheduled: {stats.get('scheduled_count', 0)}
Total Interviews Needed: {stats.get('total_variables', 0)}
Unscheduled: {stats.get('unscheduled_count', 0)}
Success Rate: {stats.get('success_rate', 0)}%
Solver Time: {stats.get('solver_time_seconds', 0)}s

{'='*60}
"""
        return summary
    
    def generate_candidate_view(self, schedule: Dict, candidate_id: str) -> str:
        """Generate schedule view for specific candidate."""
        interviews = schedule.get("interviews", [])
        cand_interviews = [i for i in interviews if i["candidate_id"] == candidate_id]
        
        if not cand_interviews:
            return f"No interviews scheduled for candidate {candidate_id}"
        
        report = f"Schedule for Candidate {candidate_id}\n" + "="*60 + "\n"
        for interview in sorted(cand_interviews, key=lambda x: x["start_time"]):
            report += f"\nInterview with {interview['interviewer_id']}\n"
            report += f"  Time: {interview['start_time']} - {interview['end_time']}\n"
            report += f"  Duration: {interview['duration_minutes']} minutes\n"
        
        return report
    
    def generate_interviewer_view(self, schedule: Dict, interviewer_id: str) -> str:
        """Generate schedule view for specific interviewer."""
        interviews = schedule.get("interviews", [])
        int_interviews = [i for i in interviews if i["interviewer_id"] == interviewer_id]
        
        if not int_interviews:
            return f"No interviews for interviewer {interviewer_id}"
        
        report = f"Schedule for Interviewer {interviewer_id}\n" + "="*60 + "\n"
        for interview in sorted(int_interviews, key=lambda x: x["start_time"]):
            report += f"\nCandidate: {interview['candidate_name']}\n"
            report += f"  Time: {interview['start_time']} - {interview['end_time']}\n"
        
        return report
    
    def generate_html_report(self, schedule: Dict, output_path: str) -> None:
        """Generate interactive HTML report."""
        interviews = schedule.get("interviews", [])
        stats = schedule.get("stats", {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Interview Schedule Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 15px; border-radius: 5px; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
        .stat-box {{ background-color: #f1f1f1; padding: 15px; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Interview Schedule Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <h3>{stats.get('scheduled_count', 0)}</h3>
            <p>Scheduled</p>
        </div>
        <div class="stat-box">
            <h3>{stats.get('total_variables', 0)}</h3>
            <p>Total Interviews Needed</p>
        </div>
        <div class="stat-box">
            <h3>{stats.get('unscheduled_count', 0)}</h3>
            <p>Unscheduled</p>
        </div>
        <div class="stat-box">
            <h3>{stats.get('success_rate', 0)}%</h3>
            <p>Success Rate</p>
        </div>
    </div>
    
    <h2>Interview Schedule</h2>
    <table>
        <tr>
            <th>Candidate</th>
            <th>Interviewer</th>
            <th>Start Time</th>
            <th>Duration</th>
        </tr>
"""
        for interview in interviews:
            html += f"""
        <tr>
            <td>{interview['candidate_name']}</td>
            <td>{interview['interviewer_id']}</td>
            <td>{interview['start_time']}</td>
            <td>{interview['duration_minutes']} min</td>
        </tr>
"""
        html += """
    </table>
</body>
</html>
"""
        with open(output_path, 'w') as f:
            f.write(html)
        logger.info(f"HTML report saved to {output_path}")
