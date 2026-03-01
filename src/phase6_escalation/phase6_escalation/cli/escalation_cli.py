# phase6_escalation/cli/escalation_cli.py

import argparse
import json

from phase6_escalation.api.escalation_api import check_query
from phase6_escalation.demo.demo_runner import run_demo
from phase6_escalation.audit.audit_cli_helpers import print_result
from phase6_escalation.audit.audit_log import EscalationAuditLog


def main():
    parser = argparse.ArgumentParser(
        description="Query Escalation Engine"
    )
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check")
    p_check.add_argument("query")
    p_check.add_argument("--json", action="store_true")

    sub.add_parser("demo")

    args = parser.parse_args()

    if args.command == "check":
        result = check_query(args.query)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_result(result)

    elif args.command == "demo":
        run_demo()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()