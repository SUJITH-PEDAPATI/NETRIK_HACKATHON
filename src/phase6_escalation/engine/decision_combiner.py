"""Combine rule-based and ML-based decisions."""

from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class CombinationStrategy(str, Enum):
    """Strategy for combining rule and ML decisions."""
    RULE_PRIMARY = "rule_primary"  # Use rule, fall back to ML
    ML_PRIMARY = "ml_primary"      # Use ML, fall back to rule
    CONSENSUS = "consensus"        # Both must agree
    MAX_CONFIDENCE = "max_confidence"  # Use highest confidence
    WEIGHTED_VOTE = "weighted_vote"    # Weighted combination
    ENSEMBLE = "ensemble"          # Average scores


@dataclass
class CombinedDecision:
    """Combined decision from rule and ML."""
    is_escalated: bool
    escalation_level: str
    final_confidence: float
    rule_decision: Optional[Dict]
    ml_decision: Optional[Dict]
    combination_rationale: str
    strategy_used: CombinationStrategy


class DecisionCombiner:
    """Combines rule-based and ML decisions."""
    
    def __init__(
        self,
        strategy: CombinationStrategy = CombinationStrategy.WEIGHTED_VOTE,
        rule_weight: float = 0.6,
        ml_weight: float = 0.4,
        confidence_threshold: float = 0.65
    ):
        """Initialize decision combiner.
        
        Args:
            strategy: How to combine decisions
            rule_weight: Weight for rule-based decision (0.0-1.0)
            ml_weight: Weight for ML decision (0.0-1.0)
            confidence_threshold: Minimum confidence for escalation
        """
        self.strategy = strategy
        self.rule_weight = rule_weight
        self.ml_weight = ml_weight
        self.confidence_threshold = confidence_threshold
    
    def combine(
        self,
        rule_result: Optional[Dict],
        ml_result: Optional[Dict]
    ) -> CombinedDecision:
        """Combine rule and ML decisions.
        
        Args:
            rule_result: Result from rule engine
            ml_result: Result from classifier engine
            
        Returns:
            CombinedDecision with final recommendation
        """
        pass
    
    def combine_scores(
        self,
        rule_score: float,
        ml_score: float,
        rule_confidence: float = 1.0,
        ml_confidence: float = 1.0
    ) -> Tuple[float, str]:
        """Combine escalation scores.
        
        Args:
            rule_score: Score from rule engine (0-1)
            ml_score: Score from ML classifier (0-1)
            rule_confidence: Confidence in rule result
            ml_confidence: Confidence in ML result
            
        Returns:
            Tuple of (final_score, rationale)
        """
        pass
    
    def apply_consensus_logic(
        self,
        rule_escalated: bool,
        ml_escalated: bool,
        rule_level: str,
        ml_level: str
    ) -> Tuple[bool, str]:
        """Apply consensus logic for agreement."""
        pass
    
    def get_combination_metrics(self) -> Dict[str, float]:
        """Get metrics about decision combinations."""
        pass
    
    def validate_combination(self, decision: CombinedDecision) -> bool:
        """Validate combined decision is valid."""
        pass
