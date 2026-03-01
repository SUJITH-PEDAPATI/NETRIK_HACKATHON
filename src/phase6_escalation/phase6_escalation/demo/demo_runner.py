# phase6_escalation/demo/demo_runner.py

from datetime import datetime
import json
import os

from phase6_escalation.engine.escalation_service import evaluate_with_context
from phase6_escalation.audit.audit_log import EscalationAuditLog
from phase6_escalation.audit.audit_cli_helpers import print_result


DEMO_QUERIES = [
    ("E001", "I want to file a lawsuit against the company."),
    ("E002", "My manager is harassing me."),
    ("E003", "When is the next team lunch?"),
]


def run_demo(log_path="./output/escalation_audit.jsonl"):

    audit = EscalationAuditLog(log_path)
    results = []

    for eid, query in DEMO_QUERIES:
        result = evaluate_with_context(
            query=query,
            employee_id=eid,
            source="demo"
        )
        audit.record(result, employee_id=eid, source="demo")
        print_result(result)
        results.append(result)

    os.makedirs("./output", exist_ok=True)
    with open("./output/escalation_demo.json", "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)