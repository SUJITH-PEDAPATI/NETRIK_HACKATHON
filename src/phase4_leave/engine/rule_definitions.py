"""Leave policy rule definitions."""


class LeaveRule:
    """Base class for leave policy rules."""
    
    def __init__(self, name, description):
        """Initialize a leave rule."""
        self.name = name
        self.description = description
    
    def apply(self, context):
        """Apply the rule to given context."""
        pass


class RuleRegistry:
    """Registry for managing leave policy rules."""
    
    def __init__(self):
        """Initialize the rule registry."""
        self.rules = {}
    
    def register_rule(self, rule):
        """Register a new rule."""
        pass
    
    def get_rule(self, name):
        """Retrieve a rule by name."""
        pass
