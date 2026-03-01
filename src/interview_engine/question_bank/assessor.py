"""
Answer Assessment and Scoring Engine
Evaluates candidate responses to interview questions
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ScoreLevel(Enum):
    """Response quality levels"""
    POOR = 1
    FAIR = 2
    GOOD = 3
    EXCELLENT = 4
    OUTSTANDING = 5


@dataclass
class AnswerAssessment:
    """Assessment of a candidate's answer"""
    question_id: str
    answer_text: str
    score_level: ScoreLevel
    confidence: float  # 0-1
    strengths: list[str]
    weaknesses: list[str]
    feedback: str
    keywords_covered: list[str]
    keywords_missing: list[str]


class AnswerAssessor:
    """Assesses and scores candidate answers"""
    
    def __init__(self):
        """Initialize assessor with evaluation criteria"""
        self.criteria_weights = {
            "completeness": 0.25,
            "structure": 0.20,
            "technical_accuracy": 0.25,
            "communication": 0.15,
            "problem_solving": 0.15,
        }
        
        self.keyword_importance = {
            "easy": 0.4,
            "medium": 0.5,
            "hard": 0.7,
        }
    
    def assess_answer(self, 
                     question_id: str,
                     question_text: str,
                     eval_hint: str,
                     answer_text: str,
                     difficulty: str) -> AnswerAssessment:
        """
        Assess a candidate's answer to a question
        
        Args:
            question_id: Question identifier
            question_text: The original question
            eval_hint: Evaluation hints with keywords/criteria
            answer_text: Candidate's answer
            difficulty: Question difficulty level
        
        Returns:
            AnswerAssessment with score and feedback
        """
        
        # Extract keywords from eval_hint
        keywords = self._extract_keywords(eval_hint)
        covered_keywords = self._find_covered_keywords(answer_text, keywords)
        missing_keywords = [k for k in keywords if k not in covered_keywords]
        
        # Calculate component scores
        completeness_score = self._score_completeness(answer_text, len(keywords))
        structure_score = self._score_structure(answer_text)
        accuracy_score = self._score_accuracy(answer_text, keywords)
        communication_score = self._score_communication(answer_text)
        problem_solving_score = self._score_problem_solving(question_text, answer_text)
        
        # Weighted final score
        final_score = (
            self.criteria_weights["completeness"] * completeness_score +
            self.criteria_weights["structure"] * structure_score +
            self.criteria_weights["technical_accuracy"] * accuracy_score +
            self.criteria_weights["communication"] * communication_score +
            self.criteria_weights["problem_solving"] * problem_solving_score
        )
        
        # Convert to score level
        score_level = self._score_to_level(final_score)
        confidence = self._calculate_confidence(final_score)
        
        # Generate feedback
        strengths = self._identify_strengths(
            completeness_score, structure_score, accuracy_score, 
            communication_score, problem_solving_score
        )
        weaknesses = self._identify_weaknesses(
            completeness_score, structure_score, accuracy_score,
            communication_score, problem_solving_score
        )
        feedback = self._generate_feedback(strengths, weaknesses, missing_keywords)
        
        return AnswerAssessment(
            question_id=question_id,
            answer_text=answer_text,
            score_level=score_level,
            confidence=confidence,
            strengths=strengths,
            weaknesses=weaknesses,
            feedback=feedback,
            keywords_covered=covered_keywords,
            keywords_missing=missing_keywords
        )
    
    def _extract_keywords(self, eval_hint: str) -> list[str]:
        """Extract keywords from evaluation hint"""
        # Split by common separators
        keywords = []
        for item in eval_hint.split(","):
            keyword = item.strip().lower()
            if keyword:
                keywords.append(keyword)
        return keywords
    
    def _find_covered_keywords(self, answer_text: str, keywords: list[str]) -> list[str]:
        """Find which keywords are mentioned in the answer"""
        answer_lower = answer_text.lower()
        covered = []
        for keyword in keywords:
            if keyword in answer_lower:
                covered.append(keyword)
        return covered
    
    def _score_completeness(self, answer_text: str, keyword_count: int) -> float:
        """Score answer completeness (0-1)"""
        word_count = len(answer_text.split())
        
        # Longer answers tend to be more complete (up to a point)
        if word_count < 50:
            return 0.3
        elif word_count < 150:
            return 0.6
        elif word_count < 300:
            return 0.85
        else:
            return 1.0
    
    def _score_structure(self, answer_text: str) -> float:
        """Score answer structure/organization (0-1)"""
        lines = answer_text.strip().split("\n")
        
        # Multiple paragraphs/sections = better structure
        if len(lines) < 2:
            return 0.4
        elif len(lines) < 5:
            return 0.6
        else:
            return 0.9
    
    def _score_accuracy(self, answer_text: str, keywords: list[str]) -> float:
        """Score technical accuracy based on keyword coverage (0-1)"""
        if not keywords:
            return 0.5
        
        covered = self._find_covered_keywords(answer_text, keywords)
        return min(1.0, len(covered) / len(keywords))
    
    def _score_communication(self, answer_text: str) -> float:
        """Score clarity of communication (0-1)"""
        # Simple heuristic: longer sentences with good structure = better communication
        sentences = answer_text.split(".")
        avg_sentence_length = len(answer_text.split()) / max(len(sentences), 1)
        
        if avg_sentence_length < 5:
            return 0.4
        elif avg_sentence_length < 15:
            return 0.8
        elif avg_sentence_length > 30:
            return 0.5  # Too long
        else:
            return 0.9
    
    def _score_problem_solving(self, question_text: str, answer_text: str) -> float:
        """Score problem-solving approach (0-1)"""
        # Look for structured thinking indicators
        indicators = [
            "first", "step", "approach", "solution", "implement",
            "consider", "alternative", "trade-off", "analyze"
        ]
        
        answer_lower = answer_text.lower()
        found_indicators = sum(1 for ind in indicators if ind in answer_lower)
        
        return min(1.0, found_indicators / 4)
    
    def _score_to_level(self, score: float) -> ScoreLevel:
        """Convert numeric score to score level"""
        if score < 0.4:
            return ScoreLevel.POOR
        elif score < 0.6:
            return ScoreLevel.FAIR
        elif score < 0.75:
            return ScoreLevel.GOOD
        elif score < 0.9:
            return ScoreLevel.EXCELLENT
        else:
            return ScoreLevel.OUTSTANDING
    
    def _calculate_confidence(self, score: float) -> float:
        """Calculate confidence in assessment (0-1)"""
        # More extreme scores = higher confidence
        return min(1.0, max(abs(score - 0.5) * 2, 0.5))
    
    def _identify_strengths(self, *scores) -> list[str]:
        """Identify answer strengths"""
        components = [
            ("Completeness", scores[0]),
            ("Structure", scores[1]),
            ("Technical Accuracy", scores[2]),
            ("Communication", scores[3]),
            ("Problem-Solving", scores[4]),
        ]
        
        strengths = []
        for name, score in components:
            if score >= 0.75:
                strengths.append(name)
        
        return strengths if strengths else ["Good attempt"]
    
    def _identify_weaknesses(self, *scores) -> list[str]:
        """Identify answer weaknesses"""
        components = [
            ("Completeness", scores[0]),
            ("Structure", scores[1]),
            ("Technical Accuracy", scores[2]),
            ("Communication", scores[3]),
            ("Problem-Solving", scores[4]),
        ]
        
        weaknesses = []
        for name, score in components:
            if score < 0.6:
                weaknesses.append(name)
        
        return weaknesses if weaknesses else []
    
    def _generate_feedback(self, strengths: list[str], 
                          weaknesses: list[str], 
                          missing_keywords: list[str]) -> str:
        """Generate actionable feedback"""
        feedback_parts = []
        
        if strengths:
            feedback_parts.append(f"Strengths: {', '.join(strengths)}")
        
        if weaknesses:
            feedback_parts.append(f"Areas to improve: {', '.join(weaknesses)}")
        
        if missing_keywords:
            feedback_parts.append(
                f"Consider mentioning: {', '.join(missing_keywords[:3])}"
            )
        
        return " | ".join(feedback_parts) if feedback_parts else "Good response"
