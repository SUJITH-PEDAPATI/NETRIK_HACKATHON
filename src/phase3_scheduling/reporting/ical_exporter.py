"""
phase3_scheduling/reporting/ical_exporter.py
──────────────────────────────────────────────
iCalendar exporter for calendar applications.
"""

from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def save_schedule_ical(result: Dict, output_path: str) -> None:
    """Save schedule to iCalendar file."""
    exporter = ICalExporter()
    exporter.export(result, output_path)


class ICalExporter:
    """Export schedule to iCalendar format."""
    
    def __init__(self, calendar_name: str = "Interview Schedule"):
        """
        Initialize iCal exporter.
        
        Args:
            calendar_name: Name for the calendar
        """
        self.calendar_name = calendar_name
        logger.info(f"Initialized ICalExporter with calendar_name={calendar_name}")
    
    def export(self, schedule: Dict, output_path: str) -> None:
        """
        Export schedule to iCalendar file.
        
        Args:
            schedule: Schedule to export
            output_path: Path to output .ics file
        """
        interviews = schedule.get("interviews", [])
        
        ical_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//HR Automation//Interview Scheduler//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Interview Schedule
X-WR-TIMEZONE:UTC
BEGIN:VTIMEZONE
TZID:UTC
BEGIN:STANDARD
DTSTART:19700101T000000
TZOFFSETFROM:+0000
TZOFFSETTO:+0000
TZNAME:UTC
END:STANDARD
END:VTIMEZONE
"""
        
        for interview in interviews:
            start_time = datetime.fromisoformat(interview["start_time"])
            end_time = datetime.fromisoformat(interview["end_time"])
            
            start_str = start_time.strftime("%Y%m%dT%H%M%SZ")
            end_str = end_time.strftime("%Y%m%dT%H%M%SZ")
            
            event = f"""BEGIN:VEVENT
UID:{interview['candidate_id']}_{interview['interviewer_id']}_{start_str}
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:Interview - {interview['candidate_name']}
DESCRIPTION:Candidate: {interview['candidate_name']}\\nInterviewer: {interview['interviewer_id']}
LOCATION:To be confirmed
STATUS:TENTATIVE
END:VEVENT
"""
            ical_content += event
        
        ical_content += "END:VCALENDAR"
        
        with open(output_path, 'w') as f:
            f.write(ical_content)
        logger.info(f"iCalendar file saved to {output_path}")
    
    def export_for_candidate(self, schedule: Dict, candidate_id: str, output_path: str) -> None:
        """Export only candidate's interviews to calendar."""
        interviews = schedule.get("interviews", [])
        cand_interviews = [i for i in interviews if i["candidate_id"] == candidate_id]
        
        schedule_filtered = {"interviews": cand_interviews}
        self.export(schedule_filtered, output_path)
        logger.info(f"Candidate calendar exported to {output_path}")
    
    def export_for_interviewer(self, schedule: Dict, interviewer_id: str, output_path: str) -> None:
        """Export only interviewer's slots to calendar."""
        interviews = schedule.get("interviews", [])
        int_interviews = [i for i in interviews if i["interviewer_id"] == interviewer_id]
        
        schedule_filtered = {"interviews": int_interviews}
        self.export(schedule_filtered, output_path)
        logger.info(f"Interviewer calendar exported to {output_path}")
    
    def generate_invite_url(self, interview: Dict) -> str:
        """Generate calendar invite URL for an interview."""
        start_time = datetime.fromisoformat(interview["start_time"])
        end_time = datetime.fromisoformat(interview["end_time"])
        
        url = f"""https://calendar.google.com/calendar/render?action=TEMPLATE
&text=Interview%20-%20{interview['candidate_name']}
&dates={start_time.strftime('%Y%m%dT%H%M%SZ')}/{end_time.strftime('%Y%m%dT%H%M%SZ')}
"""
        return url
