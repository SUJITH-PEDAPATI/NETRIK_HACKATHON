"""Rule-based escalation detection engine."""

from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class RuleOperator(str, Enum):
    """Operators for rule conditions."""
    CONTAINS = "contains"
    EXACT_MATCH = "exact_match"
    REGEX_MATCH = "regex_match"
    PHRASE_MATCH = "phrase_match"
    ANY_OF = "any_of"
    ALL_OF = "all_of"
    SCORE_ABOVE = "score_above"
    SCORE_BELOW = "score_below"


@dataclass
class EscalationRule:
    """Single escalation rule definition."""
    rule_id: str
    name: str
    description: str
    category: str
    operator: RuleOperator
    keywords: List[str]
    threshold_score: float
    escalation_level: str
    is_active: bool = True
    priority: int = 1
    applies_to_fields: List[str] = None  # ['subject', 'body', 'all']
    case_sensitive: bool = False
    requires_context: bool = False
    context_validators: List[Callable] = None


class RuleEngine:
    """Keyword and rule-based escalation detection."""
    
    def __init__(self, rules: Optional[List[EscalationRule]] = None):
        """Initialize rule engine.
        
        Args:
            rules: List of escalation rules
        """
        self.rules = rules or []
        self.rule_cache = {}
    
    def add_rule(self, rule: EscalationRule):
        """Add a new rule."""
        self.rules.append(rule)
        self._invalidate_cache()
    
    def remove_rule(self, rule_id: str):
        """Remove a rule by ID."""
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        self._invalidate_cache()
    
    def update_rule(self, rule_id: str, updates: Dict):
        """Update rule properties."""
        pass
    
    def detect(self, content: str, fields: Optional[Dict] = None) -> Dict:
        """Detect escalation based on rules.
        
        Args:
            content: Content to analyze
            fields: Additional fields for rule evaluation
            
        Returns:
            Dictionary with matched rules and scores
        """
        pass
    
    def detect_matching_rules(self, content: str) -> List[tuple[EscalationRule, float]]:
        """Get all matching rules with scores."""
        pass
    
    def get_highest_escalation_level(self, matched_rules: List[EscalationRule]) -> str:
        """Determine overall escalation level from matched rules."""
        pass
    
    def validate_rule(self, rule: EscalationRule) -> tuple[bool, List[str]]:
        """Validate rule configuration."""
        pass
    
    def _invalidate_cache(self):
        """Invalidate rule cache after modifications."""
        self.rule_cache.clear()
    
    def export_rules(self, format: str = 'json') -> str:
        """Export rules in specified format."""
        pass
    
    def import_rules(self, data: str, format: str = 'json'):
        """Import rules from data."""
        pass
