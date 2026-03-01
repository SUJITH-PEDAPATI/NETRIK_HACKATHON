"""
Interview Analytics and Reporting Engine
Generates insights and reports on candidate performance
"""

from dataclasses import dataclass
from typing import Optional
from collections import defaultdict
from .assessor import AnswerAssessment, ScoreLevel
from .evaluator import CandidateEvaluation, CandidateRating


@dataclass
class InterviewMetrics:
    """Key metrics from interview"""
    total_questions: int
    average_score: float
    median_score: float
    score_distribution: dict[str, int]  # score_level -> count
    time_per_question_avg: float
    strongest_category: str
    weakest_category: str
    technical_score: float
    behavioral_score: float
    pattern_observations: list[str]


@dataclass
class ComparisonMetrics:
    """Metrics for comparing candidates"""
    candidate_a_id: str
    candidate_b_id: str
    score_difference: float
    technical_gap: float
    behavioral_gap: float
    skill_match_comparison: dict[str, dict[str, float]]


class InterviewAnalytics:
    """Generates analytics and insights from interview data"""
    
    def __init__(self):
        """Initialize analytics engine"""
        self.interview_history: dict[str, list[CandidateEvaluation]] = defaultdict(list)
    
    def generate_metrics(self,
                        assessments: list[AnswerAssessment],
                        evaluation: CandidateEvaluation) -> InterviewMetrics:
        """
        Generate interview metrics
        
        Args:
            assessments: List of answer assessments
            evaluation: Overall candidate evaluation
        
        Returns:
            InterviewMetrics with analysis
        """
        
        # Convert scores
        score_map = {
            ScoreLevel.POOR: 0.2,
            ScoreLevel.FAIR: 0.4,
            ScoreLevel.GOOD: 0.6,
            ScoreLevel.EXCELLENT: 0.8,
            ScoreLevel.OUTSTANDING: 1.0,
        }
        
        scores = [score_map[a.score_level] for a in assessments]
        score_levels = [a.score_level for a in assessments]
        
        # Calculate statistics
        avg_score = sum(scores) / len(scores) if scores else 0
        sorted_scores = sorted(scores)
        median_score = sorted_scores[len(sorted_scores) // 2] if sorted_scores else 0
        
        # Score distribution
        distribution = defaultdict(int)
        for level in score_levels:
            distribution[level.name] += 1
        
        # Patterns
        patterns = self._identify_patterns(assessments, scores)
        
        return InterviewMetrics(
            total_questions=len(assessments),
            average_score=avg_score,
            median_score=median_score,
            score_distribution=dict(distribution),
            time_per_question_avg=evaluation.interview_duration_minutes / len(assessments) if assessments else 0,
            strongest_category=self._find_strongest_category(evaluation),
            weakest_category=self._find_weakest_category(evaluation),
            technical_score=evaluation.technical_score,
            behavioral_score=evaluation.behavioral_score,
            pattern_observations=patterns
        )
    
    def compare_candidates(self,
                          eval_a: CandidateEvaluation,
                          eval_b: CandidateEvaluation) -> ComparisonMetrics:
        """
        Compare performance of two candidates
        
        Args:
            eval_a: First candidate evaluation
            eval_b: Second candidate evaluation
        
        Returns:
            ComparisonMetrics with comparison data
        """
        
        score_difference = eval_a.overall_score - eval_b.overall_score
        technical_gap = eval_a.technical_score - eval_b.technical_score
        behavioral_gap = eval_a.behavioral_score - eval_b.behavioral_score
        
        # Skill match comparison
        skill_comparison = {}
        all_skills = set(eval_a.skill_assessments.keys()) | set(eval_b.skill_assessments.keys())
        
        for skill in all_skills:
            skill_a = eval_a.skill_assessments.get(skill)
            skill_b = eval_b.skill_assessments.get(skill)
            
            score_a = skill_a.score if skill_a else 0
            score_b = skill_b.score if skill_b else 0
            
            skill_comparison[skill] = {
                "candidate_a": score_a,
                "candidate_b": score_b,
                "gap": score_a - score_b
            }
        
        return ComparisonMetrics(
            candidate_a_id=eval_a.candidate_id,
            candidate_b_id=eval_b.candidate_id,
            score_difference=score_difference,
            technical_gap=technical_gap,
            behavioral_gap=behavioral_gap,
            skill_match_comparison=skill_comparison
        )
    
    def generate_report(self,
                       evaluation: CandidateEvaluation,
                       metrics: InterviewMetrics,
                       include_recommendations: bool = True) -> str:
        """
        Generate comprehensive interview report
        
        Args:
            evaluation: Candidate evaluation
            metrics: Interview metrics
            include_recommendations: Include hiring recommendations
        
        Returns:
            Formatted report string
        """
        
        report_lines = [
            "=" * 60,
            "INTERVIEW ASSESSMENT REPORT",
            "=" * 60,
            f"\nCandidate ID: {evaluation.candidate_id}",
            f"Overall Score: {evaluation.overall_score:.1%}",
            f"Rating: {evaluation.rating.name}",
            f"\nInterview Details:",
            f"  - Duration: {evaluation.interview_duration_minutes} minutes",
            f"  - Questions Attempted: {evaluation.total_questions_attempted}",
            f"  - Average Response Quality: {evaluation.avg_response_quality:.1%}",
        ]
        
        # Category scores
        report_lines.extend([
            f"\nCategory Scores:",
            f"  - Technical: {evaluation.technical_score:.1%}",
            f"  - Behavioral: {evaluation.behavioral_score:.1%}",
            f"  - Cultural Fit: {evaluation.cultural_fit_score:.1%}",
        ])
        
        # Skills
        report_lines.append(f"\nSkill Assessment:")
        for skill, assessment in evaluation.skill_assessments.items():
            report_lines.append(
                f"  - {skill}: {assessment.proficiency} ({assessment.score:.1%})"
            )
        
        # Strengths
        if evaluation.strengths:
            report_lines.append(f"\nStrengths:")
            for strength in evaluation.strengths:
                report_lines.append(f"  • {strength}")
        
        # Weaknesses
        if evaluation.weaknesses:
            report_lines.append(f"\nWeaknesses:")
            for weakness in evaluation.weaknesses:
                report_lines.append(f"  • {weakness}")
        
        # Concerns
        if evaluation.concerns:
            report_lines.append(f"\nConcerns:")
            for concern in evaluation.concerns:
                report_lines.append(f"  • {concern}")
        
        # Pattern observations
        if metrics.pattern_observations:
            report_lines.append(f"\nPattern Observations:")
            for pattern in metrics.pattern_observations:
                report_lines.append(f"  • {pattern}")
        
        # Recommendation
        if include_recommendations:
            report_lines.extend([
                f"\nRecommendation:",
                f"  {evaluation.recommendation}",
            ])
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def _find_strongest_category(self, evaluation: CandidateEvaluation) -> str:
        """Find strength category"""
        scores = {
            "Technical": evaluation.technical_score,
            "Behavioral": evaluation.behavioral_score,
            "Cultural Fit": evaluation.cultural_fit_score,
        }
        return max(scores, key=scores.get)
    
    def _find_weakest_category(self, evaluation: CandidateEvaluation) -> str:
        """Find weakness category"""
        scores = {
            "Technical": evaluation.technical_score,
            "Behavioral": evaluation.behavioral_score,
            "Cultural Fit": evaluation.cultural_fit_score,
        }
        return min(scores, key=scores.get)
    
    def _identify_patterns(self, 
                          assessments: list[AnswerAssessment],
                          scores: list[float]) -> list[str]:
        """Identify performance patterns"""
        patterns = []
        
        if len(scores) < 2:
            return patterns
        
        # Trending pattern
        if scores[-1] > scores[0] + 0.2:
            patterns.append("Performance improving throughout interview")
        elif scores[-1] < scores[0] - 0.2:
            patterns.append("Performance declining throughout interview")
        
        # Consistency
        variance = sum((s - sum(scores) / len(scores)) ** 2 for s in scores) / len(scores)
        if variance < 0.05:
            patterns.append("Consistent performance across questions")
        elif variance > 0.15:
            patterns.append("Highly variable performance")
        
        # Technical accuracy
        technical_keywords = sum(len(a.keywords_covered) for a in assessments)
        missing_keywords = sum(len(a.keywords_missing) for a in assessments)
        
        if missing_keywords > technical_keywords:
            patterns.append("Gaps in technical knowledge")
        elif missing_keywords == 0:
            patterns.append("Strong technical depth demonstrated")
        
        # Response quality
        quality_assessments = [a.score_level for a in assessments]
        if quality_assessments.count(ScoreLevel.OUTSTANDING) >= 2:
            patterns.append("Demonstrates exceptional problem-solving ability")
        
        return patterns
    
    def get_benchmark_comparison(self,
                                evaluation: CandidateEvaluation,
                                benchmark_avg: float = 0.65) -> dict:
        """
        Compare candidate to benchmark
        
        Args:
            evaluation: Candidate evaluation
            benchmark_avg: Average benchmark score
        
        Returns:
            Comparison metrics
        """
        
        return {
            "vs_benchmark": evaluation.overall_score - benchmark_avg,
            "percentile_estimate": self._estimate_percentile(evaluation.overall_score),
            "above_benchmark": evaluation.overall_score > benchmark_avg,
            "strengths_vs_benchmark": self._find_comparative_strengths(
                evaluation, benchmark_avg
            ),
        }
    
    def _estimate_percentile(self, score: float) -> float:
        """Estimate percentile ranking based on score"""
        # Simple linear mapping for demo purposes
        return min(100, score * 100)
    
    def _find_comparative_strengths(self, 
                                   evaluation: CandidateEvaluation,
                                   benchmark: float) -> list[str]:
        """Find areas where candidate exceeds benchmark"""
        strengths = []
        
        if evaluation.technical_score > benchmark:
            strengths.append("Above benchmark technical skills")
        
        if evaluation.behavioral_score > benchmark:
            strengths.append("Above benchmark soft skills")
        
        if evaluation.cultural_fit_score > benchmark:
            strengths.append("Strong cultural alignment")
        
        return strengths
