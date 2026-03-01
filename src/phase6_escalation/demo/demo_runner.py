"""Demo runner for escalation system features."""

from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class DemoScenario:
    """Demo scenario configuration."""
    
    scenario_id: str
    name: str
    description: str
    category: str  # 'legal', 'harassment', 'fraud', 'misc'
    sample_content: str
    expected_escalation_level: str
    expected_rules_matched: List[str]
    demo_data: Dict = None


class DemoRunner:
    """Run demonstrations of escalation system."""
    
    def __init__(self, escalation_service):
        """Initialize demo runner.
        
        Args:
            escalation_service: EscalationService instance
        """
        self.service = escalation_service
        self.demo_scenarios = []
        self.demo_results = []
        self._load_demo_scenarios()
    
    def _load_demo_scenarios(self):
        """Load predefined demo scenarios."""
        self.demo_scenarios = [
            DemoScenario(
                scenario_id="demo_001",
                name="Legal Threat Detection",
                description="Detect potential legal threats in conversation",
                category="legal",
                sample_content="I'm going to sue this company for workplace discrimination. I have documented evidence.",
                expected_escalation_level="high",
                expected_rules_matched=["legal_threat", "discrimination_keywords"]
            ),
            DemoScenario(
                scenario_id="demo_002",
                name="Harassment Report",
                description="Identify workplace harassment",
                category="harassment",
                sample_content="I've been experiencing ongoing harassment from my manager. Comments about my appearance daily.",
                expected_escalation_level="high",
                expected_rules_matched=["harassment_indicators", "workplace_conduct"]
            ),
            DemoScenario(
                scenario_id="demo_003",
                name="Financial Fraud Detection",
                description="Detect potential financial irregularities",
                category="fraud",
                sample_content="I noticed the accounting department has been moving funds between accounts fraudulently.",
                expected_escalation_level="critical",
                expected_rules_matched=["fraud_keywords", "financial_mismanagement"]
            ),
        ]
    
    def run_demo(self, scenario_id: Optional[str] = None) -> Dict:
        """Run demo scenario.
        
        Args:
            scenario_id: Specific scenario to run, or None for all
            
        Returns:
            Demo results
        """
        pass
    
    def run_all_demos(self) -> Dict:
        """Run all demo scenarios."""
        pass
    
    def run_interactive_demo(self):
        """Interactive demo mode."""
        pass
    
    def run_performance_test(self) -> Dict:
        """Run performance tests."""
        pass
    
    def run_accuracy_test(self) -> Dict:
        """Run accuracy tests against known scenarios."""
        pass
    
    def compare_detection_methods(self) -> Dict:
        """Compare rule vs ML detection."""
        pass
    
    def run_edge_case_tests(self) -> Dict:
        """Test edge cases."""
        pass
    
    def generate_demo_report(self, format: str = 'html') -> str:
        """Generate demo results report."""
        pass
    
    def stress_test(self, num_items: int = 1000) -> Dict:
        """Stress test the system."""
        pass
    
    def run_batch_demo(self) -> Dict:
        """Demonstrate batch processing."""
        pass
    
    def live_analysis_demo(self):
        """Real-time analysis demonstration."""
        pass
    
    def _create_test_case_data(self) -> Dict:
        """Create test case data."""
        pass
    
    def _print_demo_results(self, results: Dict):
        """Print formatted demo results."""
        pass
    
    def _analyze_demo_accuracy(self, results: Dict) -> Dict:
        """Analyze detection accuracy."""
        pass
    
    @staticmethod
    def get_available_demos() -> List[str]:
        """Get list of available demo scenarios."""
        return [
            "legal_threats",
            "harassment_detection",
            "fraud_detection",
            "rule_matching",
            "ml_classification",
            "batch_processing",
            "performance",
            "accuracy"
        ]
    
    @staticmethod
    def get_demo_config() -> Dict:
        """Get demo configuration."""
        return {
            "enable_ml": True,
            "rule_engine_enabled": True,
            "use_decision_combiner": True,
            "verbose_output": True,
            "save_results": True,
            "export_format": "json"
        }
