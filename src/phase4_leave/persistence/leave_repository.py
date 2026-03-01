"""Repository for leave data persistence."""

from abc import ABC, abstractmethod
from typing import List, Optional


class ILeaveRepository(ABC):
    """Interface for leave data repository."""
    
    @abstractmethod
    def create_leave_request(self, leave_request):
        """Create a new leave request."""
        pass
    
    @abstractmethod
    def get_leave_request(self, request_id):
        """Retrieve a leave request by ID."""
        pass
    
    @abstractmethod
    def update_leave_request(self, request_id, updates):
        """Update an existing leave request."""
        pass
    
    @abstractmethod
    def delete_leave_request(self, request_id):
        """Delete a leave request."""
        pass
    
    @abstractmethod
    def get_employee_leaves(self, employee_id, start_date, end_date):
        """Get all leave requests for an employee within date range."""
        pass
    
    @abstractmethod
    def get_leave_balance(self, employee_id, leave_type):
        """Get leave balance for an employee."""
        pass
    
    @abstractmethod
    def update_leave_balance(self, employee_id, leave_type, balance):
        """Update employee leave balance."""
        pass


class LeaveRepository(ILeaveRepository):
    """Implementation of leave data repository."""
    
    def __init__(self, connection=None):
        """Initialize the repository."""
        self.connection = connection
    
    def create_leave_request(self, leave_request):
        """Create a new leave request."""
        pass
    
    def get_leave_request(self, request_id):
        """Retrieve a leave request by ID."""
        pass
    
    def update_leave_request(self, request_id, updates):
        """Update an existing leave request."""
        pass
    
    def delete_leave_request(self, request_id):
        """Delete a leave request."""
        pass
    
    def get_employee_leaves(self, employee_id, start_date, end_date):
        """Get all leave requests for an employee within date range."""
        pass
    
    def get_leave_balance(self, employee_id, leave_type):
        """Get leave balance for an employee."""
        pass
    
    def update_leave_balance(self, employee_id, leave_type, balance):
        """Update employee leave balance."""
        pass
