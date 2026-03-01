"""Escalation categories and types."""

from enum import Enum


class EscalationCategory(str, Enum):
    """Main categories for escalation."""
    LEGAL = "legal"
    HARASSMENT = "harassment"
    DISCRIMINATION = "discrimination"
    HEALTH_SAFETY = "health_safety"
    FRAUD = "fraud"
    MISCONDUCT = "misconduct"
    GRIEVANCE = "grievance"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    ETHICAL = "ethical"
    OTHER = "other"


class EscalationReason(str, Enum):
    """Specific reasons for escalation."""
    LEGAL_THREAT = "legal_threat"
    HARASSMENT_ALLEGATION = "harassment_allegation"
    DISCRIMINATION_REPORT = "discrimination_report"
    WORKPLACE_INJURY = "workplace_injury"
    FINANCIAL_FRAUD = "financial_fraud"
    POLICY_VIOLATION = "policy_violation"
    FORMAL_GRIEVANCE = "formal_grievance"
    REGULATORY_BREACH = "regulatory_breach"
    DATA_BREACH = "data_breach"
    ETHICAL_VIOLATION = "ethical_violation"


class EscalationSeverity(str, Enum):
    """Severity levels for escalated cases."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class ReportingChannel(str, Enum):
    """Channels through which escalations are reported."""
    EMAIL = "email"
    PHONE = "phone"
    IN_PERSON = "in_person"
    ANONYMOUS_HOTLINE = "anonymous_hotline"
    INTERNAL_SYSTEM = "internal_system"
    EXTERNAL_AGENCY = "external_agency"
    LEGAL_COUNSEL = "legal_counsel"
    GOVERNMENT = "government"


class HandlingDepartment(str, Enum):
    """Departments handling escalations."""
    HR = "hr"
    LEGAL = "legal"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    MANAGEMENT = "management"
    EXTERNAL = "external"


class FollowUpAction(str, Enum):
    """Actions to be taken for escalation."""
    INVESTIGATION = "investigation"
    DISCIPLINARY = "disciplinary"
    MEDIATION = "mediation"
    LEGAL_REVIEW = "legal_review"
    POLICY_REVISION = "policy_revision"
    INCIDENT_REPORT = "incident_report"
    REGULATORY_NOTIFICATION = "regulatory_notification"
