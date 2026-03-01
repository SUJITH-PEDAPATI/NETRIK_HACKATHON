"""
Advanced Features and Utilities
AI-assisted evaluation and intelligent question selection
"""

from dataclasses import dataclass
from typing import Optional
from collections import Counter
import random


@dataclass
class QuestionRecommendation:
    """Recommendation for next question"""
    question_id: str
    reason: str
    priority_score: float  # 0-1
    skill_gap_importance: float
    difficulty_alignment: float


class IntelligentQuestionSelector:
    """Intelligent selection of questions based on interview context"""
    
    def __init__(self):
        """Initialize selector"""
        self.skill_weights = {}
        self.difficulty_progression = ["easy", "medium", "hard", "expert"]
    
    def recommend_question(self,
                          candidate_id: str,
                          role_required_skills: list[str],
                          answered_questions: list[dict],
                          candidate_performance: dict,
                          available_questions: list) -> QuestionRecommendation:
        """
        Recommend the best next question for the candidate
        
        Args:
            candidate_id: Candidate identifier
            role_required_skills: Required skills for the role
            answered_questions: Questions already asked
            candidate_performance: Candidate's performance metrics
            available_questions: Pool of available questions
        
        Returns:
            Top recommended question with reasoning
        """
        
        # Identify skill gaps
        covered_skills = self._extract_covered_skills(answered_questions)
        missing_skills = set(role_required_skills) - covered_skills
        
        # Determine difficulty progression
        current_avg_score = candidate_performance.get("avg_score", 0.5)
        recommended_difficulty = self._determine_difficulty(current_avg_score)
        
        # Score each available question
        recommendations = []
        
        for question in available_questions:
            # Skip if already asked
            if question.get("id") in [q.get("id") for q in answered_questions]:
                continue
            
            # Calculate scores
            skill_gap_score = self._calculate_skill_gap_score(
                question, missing_skills
            )
            difficulty_score = self._calculate_difficulty_alignment(
                question.get("difficulty"), recommended_difficulty
            )
            variety_score = self._calculate_question_variety(
                question, answered_questions
            )
            memorability_score = self._calculate_memorability(question)
            
            # Weighted priority
            priority = (
                0.4 * skill_gap_score +
                0.3 * difficulty_score +
                0.2 * variety_score +
                0.1 * memorability_score
            )
            
            recommendations.append({
                "question": question,
                "priority": priority,
                "skill_gap_score": skill_gap_score,
                "difficulty_score": difficulty_score,
                "variety_score": variety_score,
            })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x["priority"], reverse=True)
        
        if not recommendations:
            return None
        
        top = recommendations[0]
        
        return QuestionRecommendation(
            question_id=top["question"].get("id"),
            reason=self._generate_reason(top, missing_skills),
            priority_score=top["priority"],
            skill_gap_importance=top["skill_gap_score"],
            difficulty_alignment=top["difficulty_score"]
        )
    
    def _extract_covered_skills(self, answered_questions: list[dict]) -> set:
        """Extract skills covered by answered questions"""
        covered = set()
        for q in answered_questions:
            if "keywords" in q:
                covered.update(q["keywords"])
            if "skills" in q:
                covered.update(q["skills"])
        return covered
    
    def _determine_difficulty(self, avg_score: float) -> str:
        """Determine appropriate difficulty level"""
        if avg_score < 0.4:
            return "easy"
        elif avg_score < 0.65:
            return "medium"
        elif avg_score < 0.8:
            return "hard"
        else:
            return "expert"
    
    def _calculate_skill_gap_score(self, question: dict, missing_skills: set) -> float:
        """Score question based on addressing skill gaps"""
        if not missing_skills:
            return 0.5
        
        question_skills = set(question.get("skills", []))
        overlap = len(question_skills & missing_skills)
        
        return min(1.0, overlap / len(missing_skills))
    
    def _calculate_difficulty_alignment(self, q_difficulty: str, recommended: str) -> float:
        """Score question difficulty alignment"""
        if q_difficulty == recommended:
            return 1.0
        
        difficulty_levels = ["easy", "medium", "hard", "expert"]
        
        try:
            q_idx = difficulty_levels.index(q_difficulty)
            r_idx = difficulty_levels.index(recommended)
            distance = abs(q_idx - r_idx)
            
            return max(0.5, 1.0 - distance * 0.2)
        except ValueError:
            return 0.5
    
    def _calculate_question_variety(self, 
                                   question: dict,
                                   answered_questions: list[dict]) -> float:
        """Score question for variety vs. already asked"""
        # Avoid asking similar questions
        question_category = question.get("category", "")
        asked_categories = [q.get("category", "") for q in answered_questions]
        
        category_count = asked_categories.count(question_category)
        
        # Penalize if category already heavily covered
        if category_count >= 2:
            return 0.3
        elif category_count == 1:
            return 0.7
        else:
            return 1.0
    
    def _calculate_memorability(self, question: dict) -> float:
        """Score question for being memorable/distinctive"""
        text = question.get("text", "").lower()
        
        # Questions with concrete examples are more memorable
        memorable_indicators = ["example", "story", "scenario", "imagine", "design"]
        score = sum(1 for ind in memorable_indicators if ind in text) / len(memorable_indicators)
        
        return min(1.0, score)
    
    def _generate_reason(self, 
                        recommendation: dict,
                        missing_skills: set) -> str:
        """Generate human-readable reason for recommendation"""
        reasons = []
        
        if recommendation["skill_gap_score"] > 0.7:
            skills = set(recommendation["question"].get("skills", []))
            gap_skills = list(skills & missing_skills)
            if gap_skills:
                reasons.append(f"Addresses gap in {gap_skills[0]}")
        
        if recommendation["difficulty_score"] > 0.8:
            reasons.append("Difficulty well-aligned to performance")
        
        if recommendation["variety_score"] > 0.8:
            reasons.append("Good variety from previous questions")
        
        return " | ".join(reasons) if reasons else "Good overall fit"


class PerformanceAnalyzer:
    """Analyzes performance patterns and trends"""
    
    def __init__(self):
        """Initialize analyzer"""
        self.performance_history = {}
    
    def analyze_performance_trend(self, 
                                 candidate_id: str,
                                 scores: list[float]) -> dict:
        """
        Analyze performance trend
        
        Args:
            candidate_id: Candidate identifier
            scores: List of scores in order
        
        Returns:
            Trend analysis with direction and insights
        """
        
        if len(scores) < 2:
            return {"trend": "insufficient_data"}
        
        # Calculate trend
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        trend_direction = "improving" if second_avg > first_avg else "declining"
        trend_magnitude = abs(second_avg - first_avg)
        
        # Analyze consistency
        variance = self._calculate_variance(scores)
        consistency = "consistent" if variance < 0.05 else "variable"
        
        # Identify peak performance
        peak_idx = scores.index(max(scores))
        trough_idx = scores.index(min(scores))
        
        # Issue alerts
        alerts = []
        if trend_direction == "declining" and trend_magnitude > 0.15:
            alerts.append("Significant performance decline detected")
        if variance > 0.2:
            alerts.append("Highly inconsistent performance")
        if trough_idx > len(scores) / 2:
            alerts.append("Weak performance in later questions")
        
        return {
            "trend": trend_direction,
            "magnitude": trend_magnitude,
            "consistency": consistency,
            "variance": variance,
            "peak_at_question": peak_idx + 1,
            "trough_at_question": trough_idx + 1,
            "alerts": alerts,
        }
    
    def predict_success_probability(self,
                                   role_required_skill_proficiency: dict,
                                   candidate_skill_scores: dict) -> float:
        """
        Predict probability of success in role
        
        Args:
            role_required_skill_proficiency: Role requirements {skill: required_level}
            candidate_skill_scores: Candidate proficiency {skill: score}
        
        Returns:
            Success probability (0-1)
        """
        
        if not role_required_skill_proficiency:
            return 0.5
        
        proficiency_thresholds = {
            "beginner": 0.4,
            "intermediate": 0.6,
            "advanced": 0.75,
            "expert": 0.9,
        }
        
        success_scores = []
        
        for skill, required_level in role_required_skill_proficiency.items():
            candidate_score = candidate_skill_scores.get(skill, 0)
            required_threshold = proficiency_thresholds.get(required_level, 0.6)
            
            # Score for this skill requirement
            if candidate_score >= required_threshold:
                success_scores.append(1.0)
            else:
                # Partial credit for attempting the skill
                success_scores.append(candidate_score / required_threshold)
        
        # Average across all requirements
        avg_success = sum(success_scores) / len(success_scores) if success_scores else 0.5
        
        # Apply confidence penalty if critical skills missing
        critical_skills = [s for s, l in role_required_skill_proficiency.items() 
                          if l in ["advanced", "expert"]]
        critical_met = sum(1 for s in critical_skills 
                          if candidate_skill_scores.get(s, 0) >= 0.7)
        
        if critical_met < len(critical_skills) * 0.8:
            avg_success *= 0.85  # Penalty for missing critical skills
        
        return min(1.0, max(0.0, avg_success))
    
    def _calculate_variance(self, scores: list[float]) -> float:
        """Calculate variance of scores"""
        if len(scores) < 2:
            return 0
        
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        
        return variance
    
    def generate_success_factors(self,
                               evaluation,
                               benchmark_avg: float = 0.65) -> list[str]:
        """
        Generate list of factors contributing to likelihood of success
        
        Args:
            evaluation: Candidate evaluation
            benchmark_avg: Average benchmark performance
        
        Returns:
            List of success factors
        """
        
        factors = []
        
        # Strong technical foundation
        if evaluation.technical_score > benchmark_avg:
            factors.append("✓ Strong technical foundation")
        
        # Good communication
        if evaluation.behavioral_score > benchmark_avg:
            factors.append("✓ Good communication and teamwork skills")
        
        # Cultural alignment
        if evaluation.cultural_fit_score > benchmark_avg:
            factors.append("✓ Strong cultural fit")
        
        # Well-rounded
        all_scores = [
            evaluation.technical_score,
            evaluation.behavioral_score,
            evaluation.cultural_fit_score
        ]
        if len([s for s in all_scores if s > benchmark_avg]) == 3:
            factors.append("✓ Well-rounded candidate")
        
        # Problem solving
        if any("problem" in w.lower() for w in evaluation.strengths):
            factors.append("✓ Demonstrates strong problem-solving")
        
        # Learning oriented
        if any("learning" in w.lower() or "growth" in w.lower() 
               for w in evaluation.strengths):
            factors.append("✓ Demonstrates growth mindset")
        
        return factors if factors else ["Candidate shows potential"]
