"""
Candidate Evaluation Engine
Evaluates overall candidate performance across interview
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from .assessor import AnswerAssessment, ScoreLevel


class CandidateRating(Enum):
    """Overall candidate ratings"""
    STRONG_REJECT = 1
    REJECT = 2
    MAYBE = 3
    STRONG_YES = 4
    EXCEPTIONAL = 5


@dataclass
class SkillAssessment:
    """Assessment of a candidate's skill level"""
    skill: str
    score: float  # 0-1
    confidence: float  # 0-1
    proficiency: str  # beginner, intermediate, advanced, expert
    evidence: list[str]


@dataclass
class CandidateEvaluation:
    """Overall evaluation of a candidate's interview performance"""
    candidate_id: str
    overall_score: float  # 0-1
    rating: CandidateRating
    skill_assessments: dict[str, SkillAssessment]
    question_scores: dict[str, float]  # question_id -> score
    strengths: list[str]
    weaknesses: list[str]
    concerns: list[str]
    recommendation: str
    interview_duration_minutes: int
    total_questions_attempted: int
    avg_response_quality: float
    technical_score: float  # 0-1
    behavioral_score: float  # 0-1
    cultural_fit_score: float  # 0-1


class CandidateEvaluator:
    """Evaluates overall candidate performance"""
    
    def __init__(self):
        """Initialize evaluator"""
        self.skill_thresholds = {
            "expert": 0.9,
            "advanced": 0.75,
            "intermediate": 0.6,
            "beginner": 0.4,
        }
    
    def evaluate_interview(self,
                          candidate_id: str,
                          questions_asked: list[dict],
                          answer_assessments: list[AnswerAssessment],
                          required_skills: list[str],
                          interview_duration_minutes: int = 60) -> CandidateEvaluation:
        """
        Evaluate overall candidate performance
        
        Args:
            candidate_id: Candidate identifier
            questions_asked: List of questions asked (with metadata)
            answer_assessments: List of answer assessments
            required_skills: List of required skills for role
            interview_duration_minutes: Total interview duration
        
        Returns:
            CandidateEvaluation with overall scores and recommendation
        """
        
        # Calculate question scores
        question_scores = self._calculate_question_scores(answer_assessments)
        
        # Calculate category scores
        technical_score = self._calculate_category_score(
            questions_asked, answer_assessments, "technical"
        )
        behavioral_score = self._calculate_category_score(
            questions_asked, answer_assessments, "behavioral"
        )
        cultural_fit_score = self._calculate_category_score(
            questions_asked, answer_assessments, "culture_fit"
        )
        
        # Assess skills
        skill_assessments = self._assess_skills(
            answer_assessments, required_skills
        )
        
        # Calculate overall score (weighted by category)
        overall_score = (
            0.4 * technical_score +
            0.3 * behavioral_score +
            0.3 * cultural_fit_score
        )
        
        # Determine rating
        rating = self._score_to_rating(overall_score)
        
        # Identify strengths and weaknesses
        strengths = self._identify_strengths(skill_assessments, answer_assessments)
        weaknesses = self._identify_weaknesses(skill_assessments, answer_assessments)
        concerns = self._identify_concerns(
            overall_score, technical_score, behavioral_score, cultural_fit_score
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            rating, overall_score, skill_assessments, required_skills
        )
        
        avg_response_quality = sum(question_scores.values()) / len(question_scores) if question_scores else 0
        
        return CandidateEvaluation(
            candidate_id=candidate_id,
            overall_score=overall_score,
            rating=rating,
            skill_assessments=skill_assessments,
            question_scores=question_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            concerns=concerns,
            recommendation=recommendation,
            interview_duration_minutes=interview_duration_minutes,
            total_questions_attempted=len(answer_assessments),
            avg_response_quality=avg_response_quality,
            technical_score=technical_score,
            behavioral_score=behavioral_score,
            cultural_fit_score=cultural_fit_score,
        )
    
    def _calculate_question_scores(self, assessments: list[AnswerAssessment]) -> dict[str, float]:
        """Convert assessments to numeric scores"""
        scores = {}
        for assessment in assessments:
            # Convert score level to numeric
            score_map = {
                ScoreLevel.POOR: 0.2,
                ScoreLevel.FAIR: 0.4,
                ScoreLevel.GOOD: 0.6,
                ScoreLevel.EXCELLENT: 0.8,
                ScoreLevel.OUTSTANDING: 1.0,
            }
            scores[assessment.question_id] = score_map[assessment.score_level]
        return scores
    
    def _calculate_category_score(self, 
                                 questions: list[dict],
                                 assessments: list[AnswerAssessment],
                                 category: str) -> float:
        """Calculate score for a specific question category"""
        category_questions = [q for q in questions if q.get("category") == category]
        
        if not category_questions:
            return 0.5  # No questions in this category
        
        question_ids = [q["id"] for q in category_questions]
        category_assessments = [a for a in assessments if a.question_id in question_ids]
        
        if not category_assessments:
            return 0.0
        
        score_map = {
            ScoreLevel.POOR: 0.2,
            ScoreLevel.FAIR: 0.4,
            ScoreLevel.GOOD: 0.6,
            ScoreLevel.EXCELLENT: 0.8,
            ScoreLevel.OUTSTANDING: 1.0,
        }
        
        scores = [score_map[a.score_level] for a in category_assessments]
        return sum(scores) / len(scores) if scores else 0.5
    
    def _assess_skills(self, 
                      assessments: list[AnswerAssessment],
                      required_skills: list[str]) -> dict[str, SkillAssessment]:
        """Assess proficiency level for each required skill"""
        skill_assessments = {}
        
        for skill in required_skills:
            # Find assessments mentioning this skill (simplified)
            skill_lower = skill.lower()
            relevant_assessments = [
                a for a in assessments 
                if any(skill_lower in kw for kw in a.keywords_covered)
            ]
            
            if not relevant_assessments:
                skill_assessments[skill] = SkillAssessment(
                    skill=skill,
                    score=0.0,
                    confidence=0.3,
                    proficiency="beginner",
                    evidence=["No evidence of skill in interview"]
                )
                continue
            
            # Average score across relevant assessments
            score_map = {
                ScoreLevel.POOR: 0.2,
                ScoreLevel.FAIR: 0.4,
                ScoreLevel.GOOD: 0.6,
                ScoreLevel.EXCELLENT: 0.8,
                ScoreLevel.OUTSTANDING: 1.0,
            }
            
            scores = [score_map[a.score_level] for a in relevant_assessments]
            avg_score = sum(scores) / len(scores)
            
            # Determine proficiency
            proficiency = self._score_to_proficiency(avg_score)
            
            # Collect evidence
            evidence = []
            for a in relevant_assessments:
                evidence.extend(a.keywords_covered)
            
            skill_assessments[skill] = SkillAssessment(
                skill=skill,
                score=avg_score,
                confidence=0.8,
                proficiency=proficiency,
                evidence=list(set(evidence))[:3]
            )
        
        return skill_assessments
    
    def _score_to_proficiency(self, score: float) -> str:
        """Convert score to proficiency level"""
        if score < self.skill_thresholds["beginner"]:
            return "beginner"
        elif score < self.skill_thresholds["intermediate"]:
            return "intermediate"
        elif score < self.skill_thresholds["advanced"]:
            return "advanced"
        else:
            return "expert"
    
    def _score_to_rating(self, score: float) -> CandidateRating:
        """Convert overall score to rating"""
        if score < 0.3:
            return CandidateRating.STRONG_REJECT
        elif score < 0.5:
            return CandidateRating.REJECT
        elif score < 0.7:
            return CandidateRating.MAYBE
        elif score < 0.85:
            return CandidateRating.STRONG_YES
        else:
            return CandidateRating.EXCEPTIONAL
    
    def _identify_strengths(self, 
                           skill_assessments: dict[str, SkillAssessment],
                           assessments: list[AnswerAssessment]) -> list[str]:
        """Identify candidate strengths"""
        strengths = []
        
        # High-scoring skills
        for skill, assessment in skill_assessments.items():
            if assessment.score >= 0.75:
                strengths.append(f"Strong {skill} knowledge")
        
        # Common positive themes
        all_strengths = []
        for a in assessments:
            all_strengths.extend(a.strengths)
        
        favorable = {}
        for strength in all_strengths:
            favorable[strength] = favorable.get(strength, 0) + 1
        
        for strength, count in sorted(favorable.items(), key=lambda x: x[1], reverse=True)[:2]:
            if count >= 2:
                strengths.append(f"Demonstrated {strength.lower()}")
        
        return strengths[:5]
    
    def _identify_weaknesses(self,
                            skill_assessments: dict[str, SkillAssessment],
                            assessments: list[AnswerAssessment]) -> list[str]:
        """Identify candidate weaknesses"""
        weaknesses = []
        
        # Low-scoring skills
        for skill, assessment in skill_assessments.items():
            if assessment.score < 0.5:
                weaknesses.append(f"Limited {skill} experience")
        
        # Common negative themes
        all_weaknesses = []
        for a in assessments:
            all_weaknesses.extend(a.weaknesses)
        
        unfavorable = {}
        for weakness in all_weaknesses:
            unfavorable[weakness] = unfavorable.get(weakness, 0) + 1
        
        for weakness, count in sorted(unfavorable.items(), key=lambda x: x[1], reverse=True)[:2]:
            if count >= 2:
                weaknesses.append(f"Need improvement in {weakness.lower()}")
        
        return weaknesses[:5]
    
    def _identify_concerns(self, 
                          overall: float,
                          technical: float,
                          behavioral: float,
                          cultural: float) -> list[str]:
        """Identify any concerns about the candidate"""
        concerns = []
        
        if technical < 0.4:
            concerns.append("Technical skills may not meet role requirements")
        
        if behavioral < 0.4:
            concerns.append("Concerns about professional communication and collaboration")
        
        if cultural < 0.4:
            concerns.append("Potential cultural fit concerns")
        
        if overall < 0.5:
            concerns.append("Consider re-interviewing with different questions or format")
        
        return concerns
    
    def _generate_recommendation(self,
                               rating: CandidateRating,
                               overall_score: float,
                               skill_assessments: dict[str, SkillAssessment],
                               required_skills: list[str]) -> str:
        """Generate hiring recommendation"""
        
        if rating == CandidateRating.EXCEPTIONAL:
            return "STRONG HIRE - Exceptional candidate with excellent fit"
        
        if rating == CandidateRating.STRONG_YES:
            return "RECOMMEND FOR HIRE - Strong candidate with required skills"
        
        if rating == CandidateRating.MAYBE:
            # Check if critical skills are met
            critical_met = sum(1 for skill in required_skills[:3] 
                             if skill_assessments.get(skill, SkillAssessment(
                                 skill, 0, 0, "beginner", []
                             )).score >= 0.6)
            
            if critical_met >= 2:
                return "CONSIDER - Valid candidate but needs further evaluation"
            else:
                return "WEAK RECOMMENDATION - Missing critical skills"
        
        if rating == CandidateRating.REJECT:
            return "NOT RECOMMENDED - Does not meet requirements"
        
        return "STRONG REJECT - Significant gaps in core competencies"
