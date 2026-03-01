# phase6_escalation/audit/audit_cli_helpers.py

SEV_ICONS = {
    "critical": "🚨",
    "high":     "🔴",
    "medium":   "🟡",
    "low":      "🔵",
    None:       "✅",
}


def print_result(result: dict):
    esc = result["escalation"]
    sev = result.get("severity")
    icon = SEV_ICONS.get(sev, "✅") if esc else "✅"

    print("\n" + "─"*52)
    if esc:
        print(f"  {icon} ESCALATE [{sev.upper()}]")
        print(f"     Reason: {result['reason']}")
        print(f"     Category: {result.get('category')}")
        print(f"     Confidence: {result['confidence']:.0%}")
    else:
        print("  ✅ No escalation required")
        print(f"     Reason: {result['reason']}")