"""
state_management/__init__.py

Complete state management system for leave management.
"""

from .core import (
    LeaveStateMachine,
    LeaveState,
    LeaveType,
    GuardConditions,
    TransitionInfo,
    TransitionRegistry,
)

from .service import (
    StateService,
    TransitionContext,
    EventHook,
    HookRegistry,
    AuditLogger,
    AuditEntry,
)

from .persistence import (
    Repository,
    RepositoryInterface,
    MemoryStore,
    JSONStore,
    SQLiteStore,
)

from .cli import LeaveCLI, main

__all__ = [
    # Core FSM
    "LeaveStateMachine",
    "LeaveState",
    "LeaveType",
    "GuardConditions",
    "TransitionInfo",
    "TransitionRegistry",
    
    # Service layer
    "StateService",
    "TransitionContext",
    "EventHook",
    "HookRegistry",
    "AuditLogger",
    "AuditEntry",
    
    # Persistence
    "Repository",
    "RepositoryInterface",
    "MemoryStore",
    "JSONStore",
    "SQLiteStore",
    
    # CLI
    "LeaveCLI",
    "main",
]
