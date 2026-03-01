"""Logging system for audit trails and event tracking."""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path


class StructuredLogger:
    """Structured logging with JSON output."""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        """Initialize logger.
        
        Args:
            name: Logger name
            log_file: Log file path
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def log_event(
        self,
        event_type: str,
        event_data: Dict[str, Any],
        level: str = "INFO",
        user_id: Optional[str] = None
    ):
        """Log structured event.
        
        Args:
            event_type: Type of event
            event_data: Event details
            level: Log level
            user_id: User who triggered event
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "event_data": event_data,
            "user_id": user_id
        }
        
        log_message = json.dumps(event)
        
        if level == "DEBUG":
            self.logger.debug(log_message)
        elif level == "INFO":
            self.logger.info(log_message)
        elif level == "WARNING":
            self.logger.warning(log_message)
        elif level == "ERROR":
            self.logger.error(log_message)
        elif level == "CRITICAL":
            self.logger.critical(log_message)


# Global logger instance
_logger = None


def get_logger(name: str) -> StructuredLogger:
    """Get or create logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        StructuredLogger instance
    """
    global _logger
    
    if _logger is None:
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)
        
        log_file = f"logs/hr_agent_{datetime.now().strftime('%Y%m%d')}.log"
        _logger = StructuredLogger("hr_agent", log_file)
    
    return _logger


def log_event(event_type: str, event_data: Dict[str, Any], level: str = "INFO"):
    """Log event using global logger.
    
    Args:
        event_type: Type of event
        event_data: Event details
        level: Log level
    """
    logger = get_logger(__name__)
    logger.log_event(event_type, event_data, level)


def log_resume_screening(candidate_id: str, score: float, passed: bool):
    """Log resume screening event."""
    log_event("resume_screening", {
        "candidate_id": candidate_id,
        "score": score,
        "passed": passed
    })


def log_interview_scheduled(candidate_id: str, interview_date: str, interviewer: str):
    """Log interview scheduling event."""
    log_event("interview_scheduled", {
        "candidate_id": candidate_id,
        "interview_date": interview_date,
        "interviewer": interviewer
    })


def log_leave_decision(employee_id: str, leave_type: str, status: str, reason: str):
    """Log leave decision event."""
    log_event("leave_decision", {
        "employee_id": employee_id,
        "leave_type": leave_type,
        "status": status,
        "reason": reason
    })


def log_escalation(escalation_id: str, category: str, severity: str, description: str):
    """Log escalation event."""
    log_event("escalation_created", {
        "escalation_id": escalation_id,
        "category": category,
        "severity": severity,
        "description": description
    }, level="WARNING")


def log_state_transition(
    candidate_id: str,
    from_state: str,
    to_state: str,
    trigger: str,
    metadata: Optional[Dict] = None
):
    """Log state transition event."""
    log_event("state_transition", {
        "candidate_id": candidate_id,
        "from_state": from_state,
        "to_state": to_state,
        "trigger": trigger,
        "metadata": metadata or {}
    })


def log_error(error_type: str, error_message: str, context: Optional[Dict] = None):
    """Log error event."""
    log_event("error", {
        "error_type": error_type,
        "error_message": error_message,
        "context": context or {}
    }, level="ERROR")


class EventAuditTrail:
    """Collect and manage event audit trail."""
    
    def __init__(self):
        """Initialize audit trail."""
        self.events: List[Dict[str, Any]] = []
    
    def add_event(
        self,
        event_type: str,
        resource_id: str,
        action: str,
        actor_id: Optional[str] = None,
        details: Optional[Dict] = None
    ):
        """Add event to audit trail.
        
        Args:
            event_type: Type of event
            resource_id: Resource affected
            action: Action performed
            actor_id: Who performed action
            details: Additional details
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "resource_id": resource_id,
            "action": action,
            "actor_id": actor_id,
            "details": details or {}
        }
        self.events.append(event)
        log_event(event_type, event)
    
    def get_events_for_resource(self, resource_id: str) -> List[Dict]:
        """Get all events for a resource."""
        return [e for e in self.events if e["resource_id"] == resource_id]
    
    def get_events_by_actor(self, actor_id: str) -> List[Dict]:
        """Get all events by an actor."""
        return [e for e in self.events if e["actor_id"] == actor_id]
    
    def export_trail(self) -> List[Dict]:
        """Export entire audit trail."""
        return self.events
