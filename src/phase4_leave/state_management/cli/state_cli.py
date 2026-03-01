"""
state_management/cli/state_cli.py

Command-line interface for leave management.
"""

import argparse
from typing import Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class LeaveCLI:
    """Command-line interface for leave management."""
    
    def __init__(self, state_service, repository, audit_logger):
        """
        Initialize CLI.
        
        Args:
            state_service: StateService instance
            repository: Repository instance
            audit_logger: AuditLogger instance
        """
        self.state_service = state_service
        self.repository = repository
        self.audit_logger = audit_logger
    
    def submit(
        self,
        request_id: str,
        employee_id: str,
        leave_type: str,
        start_date: str,
        end_date: str,
        reason: str,
    ) -> None:
        """
        Submit a new leave request.
        
        Args:
            request_id: Request ID
            employee_id: Employee ID
            leave_type: Type of leave
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            reason: Reason for leave
        """
        request_data = {
            "request_id": request_id,
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason,
            "state": "draft",
        }
        
        # Create request
        request_id = self.state_service.create_request(request_data)
        
        # Try to transition to submitted
        success, error = self.state_service.transition(
            request_id,
            "submitted",
            employee_id,
            "employee",
            reason="CLI submission"
        )
        
        if success:
            print(f"✓ Request {request_id} submitted successfully")
        else:
            print(f"✗ Failed to submit request: {error}")
    
    def approve(
        self,
        request_id: str,
        user_id: str,
        user_role: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Approve a leave request.
        
        Args:
            request_id: Request ID
            user_id: User ID (manager or HR)
            user_role: User role (manager or hr)
            reason: Approval reason
        """
        request = self.state_service.get_request(request_id)
        if not request:
            print(f"✗ Request {request_id} not found")
            return
        
        current_state = request.get("state")
        
        # Determine target state
        if current_state == "submitted":
            target_state = "approved_manager" if user_role == "manager" else "rejected"
        elif current_state == "approved_manager":
            target_state = "approved_hr" if user_role == "hr" else "rejected"
        else:
            print(f"✗ Cannot approve request in state: {current_state}")
            return
        
        success, error = self.state_service.transition(
            request_id,
            target_state,
            user_id,
            user_role,
            reason=reason or "Approved via CLI"
        )
        
        if success:
            print(f"✓ Request {request_id} approved → {target_state}")
        else:
            print(f"✗ Approval failed: {error}")
    
    def reject(
        self,
        request_id: str,
        user_id: str,
        user_role: str,
        reason: str,
    ) -> None:
        """
        Reject a leave request.
        
        Args:
            request_id: Request ID
            user_id: User ID
            user_role: User role
            reason: Rejection reason
        """
        request = self.state_service.get_request(request_id)
        if not request:
            print(f"✗ Request {request_id} not found")
            return
        
        current_state = request.get("state")
        if current_state not in ["submitted", "approved_manager"]:
            print(f"✗ Cannot reject request in state: {current_state}")
            return
        
        success, error = self.state_service.transition(
            request_id,
            "rejected",
            user_id,
            user_role,
            reason=reason
        )
        
        if success:
            print(f"✓ Request {request_id} rejected")
        else:
            print(f"✗ Rejection failed: {error}")
    
    def cancel(
        self,
        request_id: str,
        user_id: str,
        reason: Optional[str] = None,
    ) -> None:
        """
        Cancel a leave request.
        
        Args:
            request_id: Request ID
            user_id: User ID
            reason: Cancellation reason
        """
        success, error = self.state_service.transition(
            request_id,
            "cancelled",
            user_id,
            "employee",
            reason=reason or "Cancelled via CLI"
        )
        
        if success:
            print(f"✓ Request {request_id} cancelled")
        else:
            print(f"✗ Cancellation failed: {error}")
    
    def status(self, request_id: str) -> None:
        """
        Show request status.
        
        Args:
            request_id: Request ID
        """
        request = self.state_service.get_request(request_id)
        if not request:
            print(f"✗ Request {request_id} not found")
            return
        
        print(f"\n{'='*60}")
        print(f"Request ID: {request.get('request_id')}")
        print(f"Employee: {request.get('employee_id')}")
        print(f"State: {request.get('state')}")
        print(f"Leave Type: {request.get('leave_type')}")
        print(f"Dates: {request.get('start_date')} → {request.get('end_date')}")
        print(f"Reason: {request.get('reason')}")
        print(f"Created: {request.get('created_at')}")
        print(f"Updated: {request.get('updated_at')}")
        print(f"{'='*60}\n")
    
    def history(self, request_id: str) -> None:
        """
        Show request history.
        
        Args:
            request_id: Request ID
        """
        entries = self.audit_logger.get_request_history(request_id)
        
        if not entries:
            print(f"✗ No history found for {request_id}")
            return
        
        print(f"\n{'='*80}")
        print(f"Audit History for {request_id}")
        print(f"{'='*80}")
        
        for entry in entries:
            print(f"[{entry.timestamp}] {entry.action.value}")
            if entry.user_id:
                print(f"  User: {entry.user_id} ({entry.user_role})")
            if entry.from_state and entry.to_state:
                print(f"  Transition: {entry.from_state} → {entry.to_state}")
            if entry.details:
                for key, value in entry.details.items():
                    print(f"  {key}: {value}")
            print()
        
        print(f"{'='*80}\n")
    
    def list_by_state(self, state: str) -> None:
        """
        List requests by state.
        
        Args:
            state: State to filter
        """
        requests = self.state_service.get_requests_by_state(state)
        
        if not requests:
            print(f"✗ No requests in state: {state}")
            return
        
        print(f"\n{'='*100}")
        print(f"Requests in state: {state} ({len(requests)} total)")
        print(f"{'='*100}")
        
        for req in requests:
            print(f"ID: {req.get('request_id'):20} | "
                  f"Employee: {req.get('employee_id'):15} | "
                  f"Type: {req.get('leave_type'):10} | "
                  f"Dates: {req.get('start_date')} → {req.get('end_date')}")
        
        print(f"{'='*100}\n")
    
    def list_by_employee(self, employee_id: str) -> None:
        """
        List requests by employee.
        
        Args:
            employee_id: Employee ID
        """
        requests = self.state_service.get_requests_by_employee(employee_id)
        
        if not requests:
            print(f"✗ No requests for employee: {employee_id}")
            return
        
        print(f"\n{'='*100}")
        print(f"Requests for {employee_id} ({len(requests)} total)")
        print(f"{'='*100}")
        
        for req in requests:
            print(f"ID: {req.get('request_id'):20} | "
                  f"State: {req.get('state'):15} | "
                  f"Type: {req.get('leave_type'):10} | "
                  f"Dates: {req.get('start_date')} → {req.get('end_date')}")
        
        print(f"{'='*100}\n")
    
    def stats(self) -> None:
        """Show system statistics."""
        audit_stats = self.audit_logger.get_stats()
        
        print(f"\n{'='*60}")
        print("Leave Management System Statistics")
        print(f"{'='*60}")
        print(f"Total Entries: {audit_stats['total_entries']}")
        print(f"Unique Requests: {audit_stats['unique_requests']}")
        print(f"Unique Users: {audit_stats['unique_users']}")
        print("\nActions Breakdown:")
        for action, count in audit_stats['actions'].items():
            print(f"  {action}: {count}")
        print(f"{'='*60}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Leave Management System CLI"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Submit command
    submit_parser = subparsers.add_parser("submit", help="Submit leave request")
    submit_parser.add_argument("request_id", help="Request ID")
    submit_parser.add_argument("employee_id", help="Employee ID")
    submit_parser.add_argument("leave_type", help="Leave type")
    submit_parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    submit_parser.add_argument("end_date", help="End date (YYYY-MM-DD)")
    submit_parser.add_argument("reason", help="Reason")
    
    # Approve command
    approve_parser = subparsers.add_parser("approve", help="Approve request")
    approve_parser.add_argument("request_id", help="Request ID")
    approve_parser.add_argument("user_id", help="User ID")
    approve_parser.add_argument("--role", default="manager", help="User role")
    approve_parser.add_argument("--reason", default=None, help="Reason")
    
    # Reject command
    reject_parser = subparsers.add_parser("reject", help="Reject request")
    reject_parser.add_argument("request_id", help="Request ID")
    reject_parser.add_argument("user_id", help="User ID")
    reject_parser.add_argument("--role", default="manager", help="User role")
    reject_parser.add_argument("reason", help="Reason")
    
    # Cancel command
    cancel_parser = subparsers.add_parser("cancel", help="Cancel request")
    cancel_parser.add_argument("request_id", help="Request ID")
    cancel_parser.add_argument("user_id", help="User ID")
    cancel_parser.add_argument("--reason", default=None, help="Reason")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show status")
    status_parser.add_argument("request_id", help="Request ID")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Show history")
    history_parser.add_argument("request_id", help="Request ID")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List requests")
    list_parser.add_argument("--state", default=None, help="Filter by state")
    list_parser.add_argument("--employee", default=None, help="Filter by employee")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    
    args = parser.parse_args()
    
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Would normally initialize services here
    # For now, just print help
    if not args.command:
        parser.print_help()
    else:
        print(f"Command: {args.command}")
        print("Service initialization needed for actual execution")


if __name__ == "__main__":
    main()
