"""Leave request validators."""


class LeaveValidator:
    """Validates leave requests against various criteria."""
    
    def __init__(self):
        """Initialize the validator."""
        pass
    
    def validate_dates(self, start_date, end_date):
        """Validate date range for leave request."""
        pass
    
    def validate_balance(self, employee_id, leave_type, days_requested):
        """Validate that employee has sufficient leave balance."""
        pass
    
    def validate_policy(self, leave_request):
        """Validate leave request against company policy."""
        pass
    
    def get_validation_errors(self):
        """Get all validation errors."""
        pass
