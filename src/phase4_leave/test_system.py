"""
phase4_leave/test_system.py

Integration tests for the leave management system.
"""

import pytest
from datetime import datetime, timedelta
from integration import LeaveManagementSystem


class TestLeaveManagementSystem:
    """Integration tests for leave management system."""
    
    @pytest.fixture
    def system(self):
        """Create a test system with memory storage."""
        return LeaveManagementSystem(storage_type="memory")
    
    def test_create_request(self, system):
        """Test creating a leave request."""
        request_data = {
            "request_id": "REQ-001",
            "employee_id": "EMP-001",
            "leave_type": "paid",
            "start_date": "2024-12-25",
            "end_date": "2024-12-26",
            "reason": "Holiday vacation",
        }
        
        request_id = system.create_request(request_data)
        
        assert request_id == "REQ-001"
        status = system.get_request_status(request_id)
        assert status is not None
        assert status["state"] == "draft"
        assert status["employee_id"] == "EMP-001"
    
    def test_submit_request(self, system):
        """Test submitting a request."""
        request_data = {
            "request_id": "REQ-002",
            "employee_id": "EMP-001",
            "leave_type": "paid",
            "start_date": "2025-01-10",
            "end_date": "2025-01-15",
            "reason": "Business trip",
        }
        
        request_id = system.create_request(request_data)
        success, error = system.submit_request(request_id, "EMP-001")
        
        assert success
        status = system.get_request_status(request_id)
        assert status["state"] == "submitted"
    
    def test_manager_approval(self, system):
        """Test manager approval workflow."""
        request_data = {
            "request_id": "REQ-003",
            "employee_id": "EMP-001",
            "leave_type": "sick",
            "start_date": "2025-02-01",
            "end_date": "2025-02-02",
            "reason": "Medical appointment",
        }
        
        request_id = system.create_request(request_data)
        system.submit_request(request_id, "EMP-001")
        
        success, error = system.approve_by_manager(request_id, "MGR-001")
        assert success
        
        status = system.get_request_status(request_id)
        assert status["state"] == "approved_manager"
    
    def test_full_workflow(self, system):
        """Test complete workflow: create → submit → manager approval → HR approval."""
        request_data = {
            "request_id": "REQ-004",
            "employee_id": "EMP-002",
            "leave_type": "paid",
            "start_date": "2025-03-10",
            "end_date": "2025-03-15",
            "reason": "Annual vacation",
        }
        
        # Create
        request_id = system.create_request(request_data)
        assert system.get_request_status(request_id)["state"] == "draft"
        
        # Submit
        success, _ = system.submit_request(request_id, "EMP-002")
        assert success
        assert system.get_request_status(request_id)["state"] == "submitted"
        
        # Manager approval
        success, _ = system.approve_by_manager(request_id, "MGR-001")
        assert success
        assert system.get_request_status(request_id)["state"] == "approved_manager"
        
        # HR approval
        success, _ = system.approve_by_hr(request_id, "HR-001")
        assert success
        assert system.get_request_status(request_id)["state"] == "approved_hr"
    
    def test_rejection_workflow(self, system):
        """Test rejection workflow."""
        request_data = {
            "request_id": "REQ-005",
            "employee_id": "EMP-003",
            "leave_type": "unpaid",
            "start_date": "2025-04-01",
            "end_date": "2025-04-05",
            "reason": "Personal reasons",
        }
        
        request_id = system.create_request(request_data)
        system.submit_request(request_id, "EMP-003")
        
        success, _ = system.reject_request(
            request_id,
            "MGR-001",
            "manager",
            reason="Budget constraints"
        )
        
        assert success
        status = system.get_request_status(request_id)
        assert status["state"] == "rejected"
    
    def test_cancellation_workflow(self, system):
        """Test request cancellation."""
        request_data = {
            "request_id": "REQ-006",
            "employee_id": "EMP-004",
            "leave_type": "personal",
            "start_date": "2025-05-10",
            "end_date": "2025-05-12",
            "reason": "Personal time",
        }
        
        request_id = system.create_request(request_data)
        system.submit_request(request_id, "EMP-004")
        
        success, _ = system.cancel_request(
            request_id,
            "EMP-004",
            reason="Plans changed"
        )
        
        assert success
        status = system.get_request_status(request_id)
        assert status["state"] == "cancelled"
    
    def test_audit_trail(self, system):
        """Test audit trail tracking."""
        request_data = {
            "request_id": "REQ-007",
            "employee_id": "EMP-005",
            "leave_type": "paid",
            "start_date": "2025-06-01",
            "end_date": "2025-06-05",
            "reason": "Summer vacation",
        }
        
        request_id = system.create_request(request_data)
        system.submit_request(request_id, "EMP-005")
        system.approve_by_manager(request_id, "MGR-001")
        
        history = system.get_request_history(request_id)
        
        assert len(history) > 0
        # Filter for transition entries
        transitions = [e for e in history if e.action.value == "transitioned"]
        assert len(transitions) >= 1
    
    def test_statistics(self, system):
        """Test system statistics."""
        # Create a few requests
        for i in range(3):
            request_data = {
                "request_id": f"REQ-{1000+i}",
                "employee_id": f"EMP-{100+i}",
                "leave_type": "paid",
                "start_date": "2025-07-01",
                "end_date": "2025-07-05",
                "reason": "Vacation",
            }
            request_id = system.create_request(request_data)
            system.submit_request(request_id, f"EMP-{100+i}")
        
        stats = system.get_system_stats()
        
        assert "audit" in stats
        assert "storage" in stats
        assert stats["audit"]["total_entries"] > 0
        assert stats["audit"]["unique_requests"] >= 3
    
    def test_multiple_employees(self, system):
        """Test handling multiple employees."""
        employees = ["EMP-A", "EMP-B", "EMP-C"]
        
        for emp_id in employees:
            request_data = {
                "request_id": f"REQ-{emp_id}",
                "employee_id": emp_id,
                "leave_type": "paid",
                "start_date": "2025-08-01",
                "end_date": "2025-08-05",
                "reason": f"Vacation for {emp_id}",
            }
            system.create_request(request_data)
        
        # All requests should be created successfully
        stats = system.get_system_stats()
        assert stats["audit"]["unique_requests"] >= len(employees)
    
    def test_error_handling(self, system):
        """Test error handling for invalid requests."""
        request_data = {
            "request_id": "REQ-ERR",
            "employee_id": "EMP-ERR",
            "leave_type": "paid",
            "start_date": "2025-09-01",
            "end_date": "2025-09-05",
            "reason": "Error test",
        }
        
        request_id = system.create_request(request_data)
        
        # Try to transition to invalid state
        success, error = system.service.transition(
            request_id,
            "invalid_state",
            "EMP-ERR",
            "employee",
        )
        
        assert not success
        assert error is not None


class TestCLIInterface:
    """Tests for CLI interface."""
    
    @pytest.fixture
    def system(self):
        """Create a test system."""
        return LeaveManagementSystem(storage_type="memory")
    
    def test_cli_submit(self, system, capsys):
        """Test CLI submit command."""
        system.cli.submit(
            "REQ-CLI-001",
            "EMP-001",
            "paid",
            "2025-10-01",
            "2025-10-05",
            "Vacation"
        )
        
        captured = capsys.readouterr()
        assert "submitted" in captured.out.lower() or "success" in captured.out.lower()
    
    def test_cli_status(self, system, capsys):
        """Test CLI status command."""
        request_data = {
            "request_id": "REQ-CLI-002",
            "employee_id": "EMP-001",
            "leave_type": "paid",
            "start_date": "2025-11-01",
            "end_date": "2025-11-05",
            "reason": "Vacation",
        }
        
        request_id = system.create_request(request_data)
        system.cli.status(request_id)
        
        captured = capsys.readouterr()
        assert "REQ-CLI-002" in captured.out


# Manual test function for standalone execution
def manual_test():
    """Manual test for standalone execution."""
    print("=" * 80)
    print("Leave Management System - Manual Test")
    print("=" * 80)
    
    # Initialize system
    system = LeaveManagementSystem(storage_type="memory")
    print("\n✓ System initialized")
    
    # Create request
    request_data = {
        "request_id": "REQ-MANUAL-001",
        "employee_id": "EMP-JOHN",
        "leave_type": "paid",
        "start_date": "2025-12-20",
        "end_date": "2025-12-31",
        "reason": "Year-end vacation",
    }
    
    request_id = system.create_request(request_data)
    print(f"✓ Created request: {request_id}")
    
    # Submit
    success, error = system.submit_request(request_id, "EMP-JOHN")
    print(f"✓ Submitted request: {success}")
    
    # Manager approval
    success, error = system.approve_by_manager(request_id, "MGR-JANE")
    print(f"✓ Manager approved: {success}")
    
    # HR approval
    success, error = system.approve_by_hr(request_id, "HR-BOB")
    print(f"✓ HR approved: {success}")
    
    # Check final status
    status = system.get_request_status(request_id)
    print(f"\n✓ Final Status: {status['state']}")
    print(f"  Employee: {status['employee_id']}")
    print(f"  Dates: {status['start_date']} → {status['end_date']}")
    print(f"  Reason: {status['reason']}")
    
    # Show history
    history = system.get_request_history(request_id)
    print(f"\n✓ Audit History ({len(history)} entries):")
    for entry in history:
        print(f"  [{entry.timestamp}] {entry.action.value}")
    
    # Show stats
    stats = system.get_system_stats()
    print(f"\n✓ System Stats:")
    print(f"  Total Audit Entries: {stats['audit']['total_entries']}")
    print(f"  Unique Requests: {stats['audit']['unique_requests']}")
    print(f"  Unique Users: {stats['audit']['unique_users']}")
    
    print("\n" + "=" * 80)
    print("Manual test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    # Run manual test
    manual_test()
