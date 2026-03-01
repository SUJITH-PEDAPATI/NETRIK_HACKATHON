"""
phase4_leave/README.md

Leave Management System - Phase 4
"""

# Leave Management System (Phase 4)

Advanced state management system for employee leave requests with comprehensive workflow automation.

## Architecture

```
phase4_leave/
├── state_management/
│   ├── core/              # Pure FSM logic
│   │   ├── fsm_definition.py   # State machine and request models
│   │   ├── guards.py           # Transition guard conditions
│   │   └── transitions.py      # Transition metadata and registry
│   │
│   ├── service/           # Runtime execution layer
│   │   ├── state_service.py    # Main service executor
│   │   ├── event_hooks.py      # Lifecycle hooks
│   │   └── audit_logger.py     # Audit trail logging
│   │
│   ├── persistence/       # Storage layer
│   │   ├── repository.py       # Abstract interface
│   │   ├── memory_store.py     # In-memory storage
│   │   ├── json_store.py       # JSON file storage
│   │   └── sqlite_store.py     # SQLite database storage
│   │
│   └── cli/               # Command-line interface
│       └── state_cli.py   # CLI commands
│
└── integration.py         # System integration layer
```

## States

1. **DRAFT** - Initial state when request is created
2. **SUBMITTED** - Request submitted for approval
3. **APPROVED_MANAGER** - Approved by direct manager
4. **APPROVED_HR** - Approved by HR department
5. **REJECTED** - Request rejected
6. **CANCELLED** - Request cancelled
7. **COMPLETED** - Leave period completed
8. **FAILED** - Processing error (recovery point)

## Leave Types

- PAID - Paid leave
- UNPAID - Unpaid leave
- SICK - Sick leave
- PERSONAL - Personal leave
- BEREAVEMENT - Bereavement leave
- MATERNITY - Maternity leave
- SABBATICAL - Sabbatical leave

## Core Components

### 1. FSM Definition (core/fsm_definition.py)

Defines the finite state machine with all valid state transitions.

```python
fsm = LeaveStateMachine()
valid_next = fsm.get_valid_transitions("submitted")
# Returns: ["approved_manager", "rejected", "cancelled"]
```

### 2. Guard Conditions (core/guards.py)

Pre-transition validation rules:

- `has_balance()` - Employee has sufficient leave balance
- `no_overlapping_leaves()` - No conflicts with other leaves
- `valid_leave_period()` - Leave dates are in the future
- `team_coverage()` - Minimum team coverage maintained
- `manager_approval_required()` - User is manager
- `hr_approval_required()` - User is HR

```python
guard_registry = GuardRegistry()
result = guard_registry.evaluate_guard("has_balance", request, context)
if not result.allowed:
    print(f"Guard failed: {result.reason}")
```

### 3. Transitions (core/transitions.py)

Metadata for state transitions including:
- Required guards
- Required roles
- Lifecycle hooks (on_enter, on_exit)

```python
transition_registry = TransitionRegistry()
transition = transition_registry.get_transition("submitted", "approved_manager")
# transition.required_guards: ["has_balance", "no_overlapping_leaves", "team_coverage"]
# transition.required_role: "manager"
```

### 4. State Service (service/state_service.py)

Runtime service that executes transitions:

```python
service = StateService(fsm, guard_registry, transition_registry, hook_registry, audit_logger)

# Check if transition is allowed
allowed, reasons = service.can_transition(
    request_id="REQ-001",
    to_state="approved_manager",
    user_id="MGR-001",
    user_role="manager",
)

# Execute transition
success, error = service.transition(
    request_id="REQ-001",
    to_state="approved_manager",
    user_id="MGR-001",
    user_role="manager",
    reason="Approved"
)
```

### 5. Event Hooks (service/event_hooks.py)

Lifecycle hooks for side effects:

- `validate_request` - Validate on submission
- `notify_approval` - Notify on approval
- `notify_rejection` - Notify on rejection
- `allocate_leave_balance` - Allocate balance
- `restore_balance` - Restore on cancellation
- `generate_summary` - Generate completion summary
- `reset_request` - Reset for recovery

```python
hook_registry = HookRegistry()
hook_registry.execute_hook("allocate_leave_balance", "enter", context, request)
```

### 6. Audit Logger (service/audit_logger.py)

Comprehensive audit trail of all transitions:

```python
audit_logger = AuditLogger()
audit_logger.log_transition(context)
history = audit_logger.get_request_history("REQ-001")
stats = audit_logger.get_stats()
audit_logger.export_to_json("audit.json")
```

### 7. Persistence Layer (persistence/)

Multiple storage backends:

#### Memory Store (Dev/Testing)
```python
store = MemoryStore()
store.save("REQ-001", request_data)
request = store.load("REQ-001")
```

#### JSON Store (File-based)
```python
store = JSONStore("leave_requests.json")
store.save("REQ-001", request_data)
```

#### SQLite Store (Production)
```python
store = SQLiteStore("leave_management.db")
store.save("REQ-001", request_data)
stats = store.get_stats()
```

### 8. CLI Interface (cli/state_cli.py)

Command-line interface for operations:

```python
cli = LeaveCLI(state_service, repository, audit_logger)

# Submit request
cli.submit("REQ-001", "EMP-001", "paid", "2024-12-25", "2024-12-26", "Vacation")

# Approve
cli.approve("REQ-001", "MGR-001", "manager", reason="Approved")

# Reject
cli.reject("REQ-001", "MGR-001", "manager", reason="Budget constraints")

# Cancel
cli.cancel("REQ-001", "EMP-001", reason="Plan changed")

# View status
cli.status("REQ-001")

# View history
cli.history("REQ-001")

# List requests
cli.list_by_state("submitted")
cli.list_by_employee("EMP-001")

# View statistics
cli.stats()
```

## Integration Example

Use the integrated system:

```python
from phase4_leave.integration import LeaveManagementSystem

# Initialize with in-memory storage
system = LeaveManagementSystem(storage_type="memory")

# Create request
request_id = system.create_request({
    "request_id": "REQ-001",
    "employee_id": "EMP-001",
    "leave_type": "paid",
    "start_date": "2024-12-25",
    "end_date": "2024-12-26",
    "reason": "Holiday vacation",
})

# Submit
success, error = system.submit_request(request_id, "EMP-001")

# Manager approves
success, error = system.approve_by_manager(request_id, "MGR-001")

# HR approves
success, error = system.approve_by_hr(request_id, "HR-001")

# Check status
status = system.get_request_status(request_id)

# Get history
history = system.get_request_history(request_id)

# Get statistics
stats = system.get_system_stats()
```

## Workflow Example

```
Employee creates request
         ↓
     [DRAFT]
         ↓
Employee submits
         ↓
    [SUBMITTED] ← (guards: has_balance, no_overlap, coverage)
         ↓
Manager reviews
    ├→ [APPROVED_MANAGER] ← manager approval
    ├→ [REJECTED] ← manager rejection
    └→ [CANCELLED]
         ↓
         (if approved_manager)
HR reviews
    ├→ [APPROVED_HR] ← HR approval + allocate balance
    ├→ [REJECTED] ← HR rejection + notify
    └→ [CANCELLED] ← restore balance
         ↓
         (if approved_hr)
    [COMPLETED] ← Leave period ends, balance deducted
```

## Guard Conditions

Transitions are protected by guards that ensure business rules:

1. **has_balance** - Employee must have sufficient leave balance
2. **no_overlapping_leaves** - No overlapping approved leaves in requested period
3. **valid_leave_period** - Leave must not be in the past
4. **team_coverage** - At least 1 person per team must be working
5. **manager_approval_required** - Only managers can approve at this stage
6. **hr_approval_required** - Only HR can approve at this stage

## Event Hooks

Hooks execute side effects during transitions:

- **on_exit** hooks execute when leaving a state
- **on_enter** hooks execute when entering a state

Common hooks:
- Notifications to stakeholders
- Balance updates
- Audit logging
- Email alerts
- Integration with other systems

## Error Handling

- Transition failure reasons are detailed
- FAILED state available for error recovery
- Audit log tracks all failures
- Detailed error messages guide users

## Features

✅ Finite State Machine for workflow control
✅ Guard conditions for rule enforcement
✅ Event hooks for side effects
✅ Audit logging of all transitions
✅ Multiple storage backends
✅ Transaction-safe operations
✅ Role-based access control
✅ Comprehensive error handling
✅ CLI interface for users
✅ Extensible architecture

## Testing

The system is designed for easy testing:

```python
import pytest
from phase4_leave.integration import LeaveManagementSystem

def test_leave_workflow():
    system = LeaveManagementSystem(storage_type="memory")
    
    # Create request
    req_id = system.create_request({...})
    
    # Submit
    success, error = system.submit_request(req_id, "EMP-001")
    assert success
    
    # Manager approves
    success, error = system.approve_by_manager(req_id, "MGR-001")
    assert success
    
    # Verify state
    status = system.get_request_status(req_id)
    assert status["state"] == "approved_manager"
```

## Future Enhancements

- Bulk operations (approve multiple requests)
- Workflow templates (different approval chains for different leave types)
- Delegation (manager delegation to another manager)
- Scheduling optimization (suggest best leave dates)
- Integration with calendar systems
- Mobile app support
- Advanced reporting and analytics
