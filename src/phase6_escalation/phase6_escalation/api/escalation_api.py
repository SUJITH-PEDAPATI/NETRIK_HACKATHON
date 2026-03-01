# phase6_escalation/api/escalation_api.py

from phase6_escalation.engine.escalation_service import (
    evaluate,
    evaluate_with_context
)
from phase6_escalation.audit.audit_log import EscalationAuditLog

DEFAULT_LOG = "./output/escalation_audit.jsonl"


def check_query(
    query: str,
    log: bool = True,
    source: str = "api",
    employee_id: str = None,
    log_path: str = DEFAULT_LOG,
) -> dict:
    result = evaluate(query)
    if log:
        EscalationAuditLog(log_path).record(
            result,
            employee_id=employee_id,
            source=source
        )
    return result


def check_query_with_context(
    query: str,
    employee_id: str = None,
    employee_name: str = None,
    source: str = "chatbot",
    metadata: dict = None,
    log: bool = True,
    log_path: str = DEFAULT_LOG,
) -> dict:
    result = evaluate_with_context(
        query=query,
        employee_id=employee_id,
        employee_name=employee_name,
        source=source,
        metadata=metadata,
    )
    if log:
        EscalationAuditLog(log_path).record(
            result,
            employee_id=employee_id,
            source=source
        )
    return result