"""Escalation configuration and keyword mappings."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .escalation_types import EscalationCategory, EscalationSeverity


@dataclass
class KeywordMapping:
    """Mapping of keywords to escalation categories."""
    
    category: EscalationCategory
    keywords: List[str]
    severity_keywords: Dict[EscalationSeverity, List[str]] = field(default_factory=dict)
    context_modifiers: Dict[str, float] = field(default_factory=dict)  # word: score modifier
    phrase_keywords: List[str] = field(default_factory=list)
    regex_patterns: List[str] = field(default_factory=list)
    weight: float = 1.0
    is_active: bool = True


@dataclass
class EscalationThreshold:
    """Thresholds for escalation decision."""
    
    low_threshold: float = 0.3
    medium_threshold: float = 0.5
    high_threshold: float = 0.7
    critical_threshold: float = 0.85
    min_confidence_for_escalation: float = 0.65
    ml_confidence_weight: float = 0.4
    rule_confidence_weight: float = 0.6


@dataclass
class SLAConfiguration:
    """Service Level Agreement settings."""
    
    category: EscalationCategory
    response_sla_hours: int
    resolution_sla_hours: int
    escalation_to_external_hours: int
    priority_notification_hours: int


@dataclass
class EscalationConfig:
    """Main escalation system configuration."""
    
    system_name: str = "HR Escalation System"
    version: str = "1.0"
    enable_auto_detection: bool = True
    enable_ml_classifier: bool = False
    ml_model_type: Optional[str] = None  # 'llm', 'ml', 'hybrid'
    rule_engine_threshold: float = 0.6
    ml_engine_threshold: float = 0.65
    use_combined_decision: bool = True
    decision_strategy: str = "weighted_vote"  # rule_primary, ml_primary, consensus, etc.
    
    keyword_mappings: List[KeywordMapping] = field(default_factory=list)
    thresholds: EscalationThreshold = field(default_factory=EscalationThreshold)
    sla_configs: Dict[str, SLAConfiguration] = field(default_factory=dict)
    
    # Notification configuration
    notify_by_default: bool = True
    notification_channels: List[str] = field(default_factory=lambda: ["email", "system"])
    escalation_notification_delay_minutes: int = 5
    
    # Audit and compliance
    enable_audit_logging: bool = True
    audit_log_retention_days: int = 2555  # 7 years
    anonymize_sensitive_data: bool = False
    
    # Routing configuration
    default_handling_department: str = "HR"
    route_to_legal_threshold: float = 0.8
    route_to_compliance_threshold: float = 0.75
    route_to_security_threshold: float = 0.7
    
    # Custom settings
    max_case_references: int = 5
    enable_case_linking: bool = True
    auto_mark_duplicate: bool = True
    similarity_threshold_for_duplicate: float = 0.85
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize created_at if not set."""
        if self.created_at is None:
            from datetime import datetime
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
    
    def get_sla_for_category(self, category: EscalationCategory) -> Optional[SLAConfiguration]:
        """Get SLA configuration for escalation category."""
        return self.sla_configs.get(category.value)
    
    def get_keywords_for_category(self, category: EscalationCategory) -> List[str]:
        """Get keywords for specific category."""
        for mapping in self.keyword_mappings:
            if mapping.category == category:
                return mapping.keywords
        return []


@dataclass
class EscalationRuleConfig:
    """Configuration for individual escalation rules."""
    
    rule_id: str
    rule_name: str
    description: str
    category: EscalationCategory
    keywords: List[str]
    severity_level: EscalationSeverity
    requires_human_review: bool = False
    auto_escalate: bool = True
    notify_on_match: bool = True
    confidence_boost: float = 0.0  # Additional confidence to add
    context_required: bool = False
    min_matches_required: int = 1
    is_active: bool = True
    created_at: Optional[datetime] = None


from datetime import datetime
