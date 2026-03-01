"""Decision explanation engine for interpretability."""

from typing import Dict, Any, List, Optional
from datetime import datetime


class ExplanationEngine:
    """Generate human-readable explanations for system decisions."""
    
    def __init__(self):
        """Initialize explanation engine."""
        self.decision_explanations = {}
    
    def explain_resume_score(
        self,
        candidate_name: str,
        score: float,
        factors: Dict[str, float]
    ) -> str:
        """Explain resume screening score.
        
        Args:
            candidate_name: Candidate name
            score: Final score
            factors: Score factors and weights
            
        Returns:
            Explanation text
        """
        explanation = f"""
## Resume Screening Decision for {candidate_name}

**Final Score: {score}/100**

### Score Breakdown:
"""
        for factor, value in factors.items():
            explanation += f"- **{factor}**: {value:.1f}%\n"
        
        recommendation = "✅ RECOMMENDED" if score >= 85 else ("⏳ REVIEW" if score >= 70 else "❌ NOT RECOMMENDED")
        explanation += f"\n### Recommendation: {recommendation}\n"
        
        return explanation
    
    def explain_leave_decision(
        self,
        employee_name: str,
        decision: str,
        policy_checks: Dict[str, bool],
        balance_info: Dict[str, float]
    ) -> str:
        """Explain leave request decision.
        
        Args:
            employee_name: Employee name
            decision: Approved/Rejected
            policy_checks: Policy validation results
            balance_info: Leave balance information
            
        Returns:
            Explanation text
        """
        explanation = f"""
## Leave Request Decision for {employee_name}

**Decision: {decision}**

### Policy Checks:
"""
        for check, passed in policy_checks.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            explanation += f"- {check}: {status}\n"
        
        explanation += "\n### Leave Balance:\n"
        for balance_type, days in balance_info.items():
            explanation += f"- {balance_type}: {days} days\n"
        
        return explanation
    
    def explain_scheduling_conflict(
        self,
        conflict_type: str,
        candidates: List[str],
        dates: List[str],
        resolution: str
    ) -> str:
        """Explain scheduling conflict and resolution.
        
        Args:
            conflict_type: Type of conflict
            candidates: Affected candidates
            dates: Conflicting dates
            resolution: How it was resolved
            
        Returns:
            Explanation text
        """
        explanation = f"""
## Scheduling Conflict Resolution

**Conflict Type: {conflict_type}**

### Affected Candidates:
"""
        for candidate in candidates:
            explanation += f"- {candidate}\n"
        
        explanation += "\n### Conflicting Dates:\n"
        for date in dates:
            explanation += f"- {date}\n"
        
        explanation += f"\n### Resolution: {resolution}\n"
        
        return explanation
    
    def explain_escalation(
        self,
        escalation_id: str,
        severity: str,
        triggers: List[str],
        recommended_actions: List[str]
    ) -> str:
        """Explain escalation trigger and actions.
        
        Args:
            escalation_id: Escalation ID
            severity: Escalation severity
            triggers: What triggered escalation
            recommended_actions: Recommended follow-up actions
            
        Returns:
            Explanation text
        """
        explanation = f"""
## Escalation Report: {escalation_id}

**Severity: {severity}**

### Escalation Triggers:
"""
        for i, trigger in enumerate(triggers, 1):
            explanation += f"{i}. {trigger}\n"
        
        explanation += "\n### Recommended Actions:\n"
        for i, action in enumerate(recommended_actions, 1):
            explanation += f"{i}. {action}\n"
        
        return explanation


# Global engine instance
_engine = ExplanationEngine()


def get_decision_explanation(
    decision_type: str,
    data: Dict[str, Any]
) -> str:
    """Get explanation for a decision.
    
    Args:
        decision_type: Type of decision (resume_score, leave_decision, etc.)
        data: Decision data
        
    Returns:
        Explanation text
    """
    engine = _engine
    
    if decision_type == "resume_score":
        return engine.explain_resume_score(
            data.get("candidate_name", "Unknown"),
            data.get("score", 0),
            data.get("factors", {})
        )
    
    elif decision_type == "leave_request":
        return engine.explain_leave_decision(
            data.get("employee_name", "Unknown"),
            data.get("decision", "Pending"),
            data.get("policy_checks", {}),
            data.get("balance_info", {})
        )
    
    elif decision_type == "scheduling_conflict":
        return engine.explain_scheduling_conflict(
            data.get("conflict_type", "Unknown"),
            data.get("candidates", []),
            data.get("dates", []),
            data.get("resolution", "Pending")
        )
    
    elif decision_type == "escalation":
        return engine.explain_escalation(
            data.get("escalation_id", "Unknown"),
            data.get("severity", "Unknown"),
            data.get("triggers", []),
            data.get("recommended_actions", [])
        )
    
    return "No explanation available for this decision type."


def format_explanation_markdown(explanation: str) -> str:
    """Format explanation as markdown."""
    return explanation


def generate_decision_report(
    decision_id: str,
    decision_data: Dict[str, Any],
    explanation: str
) -> Dict[str, Any]:
    """Generate complete decision report.
    
    Args:
        decision_id: Decision identifier
        decision_data: Decision data
        explanation: Decision explanation
        
    Returns:
        Complete report dictionary
    """
    return {
        "decision_id": decision_id,
        "timestamp": datetime.now().isoformat(),
        "decision_data": decision_data,
        "explanation": explanation,
        "confidence_score": decision_data.get("confidence", 0.85)
    }
