"""
Adaptive Interview Engine
Dynamically adjusts interview difficulty and questions based on candidate performance
"""

from dataclasses import dataclass
from typing import Optional
from .models import Question
from .assessor import AnswerAssessment, AnswerAssessor, ScoreLevel


@dataclass
class InterviewSession:
    """Tracks an active interview session"""
    session_id: str
    candidate_id: str
    role_required_skills: list[str]
    total_questions: int
    questions_asked: list[Question] = None
    current_question_index: int = 0
    assessments: list[AnswerAssessment] = None
    current_difficulty: str = "medium"
    is_complete: bool = False
    
    def __post_init__(self):
        if self.questions_asked is None:
            self.questions_asked = []
        if self.assessments is None:
            self.assessments = []


class AdaptiveInterviewEngine:
    """Manages adaptive interview flow"""
    
    def __init__(self, question_registry):
        """
        Initialize adaptive engine
        
        Args:
            question_registry: Registry to pull questions from
        """
        self.question_registry = question_registry
        self.assessor = AnswerAssessor()
        self.sessions: dict[str, InterviewSession] = {}
        
        # Difficulty progression thresholds
        self.difficulty_thresholds = {
            "easy_to_medium": 0.7,      # If scoring >70% on easy, move to medium
            "medium_to_hard": 0.75,     # If scoring >75% on medium, move to hard
            "hard_to_expert": 0.8,      # If scoring >80% on hard, move to expert
            "downgrade_threshold": 0.4, # If scoring <40%, downgrade difficulty
        }
    
    def create_session(self,
                      session_id: str,
                      candidate_id: str,
                      role_required_skills: list[str],
                      total_questions: int = 8) -> InterviewSession:
        """Create a new adaptive interview session"""
        session = InterviewSession(
            session_id=session_id,
            candidate_id=candidate_id,
            role_required_skills=role_required_skills,
            total_questions=total_questions,
            current_difficulty="medium"
        )
        
        self.sessions[session_id] = session
        return session
    
    def get_next_question(self, session_id: str) -> Optional[Question]:
        """
        Get the next adapted question for the candidate
        
        Args:
            session_id: Current interview session ID
        
        Returns:
            Next adapted question or None if interview complete
        """
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        # Check if interview is complete
        if session.current_question_index >= session.total_questions:
            session.is_complete = True
            return None
        
        # Get next question with adaptive difficulty
        question = self._select_adaptive_question(session)
        
        if question:
            session.questions_asked.append(question)
            session.current_question_index += 1
        
        return question
    
    def submit_answer(self,
                     session_id: str,
                     answer_text: str) -> AnswerAssessment:
        """
        Submit candidate answer and receive assessment
        
        Args:
            session_id: Current interview session ID
            answer_text: Candidate's answer to current question
        
        Returns:
            AnswerAssessment with score
        """
        session = self.sessions.get(session_id)
        if not session or not session.questions_asked:
            return None
        
        # Get current question
        current_question = session.questions_asked[-1]
        
        # Assess answer
        assessment = self.assessor.assess_answer(
            question_id=current_question.id,
            question_text=current_question.text,
            eval_hint=current_question.eval_hint or "",
            answer_text=answer_text,
            difficulty=current_question.difficulty
        )
        
        session.assessments.append(assessment)
        
        # Adapt difficulty based on performance
        self._adapt_difficulty(session)
        
        return assessment
    
    def _select_adaptive_question(self, session: InterviewSession) -> Optional[Question]:
        """
        Select next question adaptively based on performance
        
        Strategy:
        1. Start with medium difficulty
        2. Vary by required skills
        3. Adjust difficulty based on recent performance
        """
        
        # Calculate recent performance
        recent_score = self._calculate_recent_performance(session)
        
        # Determine next difficulty
        difficulty = self._determine_next_difficulty(recent_score, session.current_difficulty)
        session.current_difficulty = difficulty
        
        # Select question matching skill and difficulty
        # First, prioritize missing skills
        covered_skills = set()
        for assessment in session.assessments:
            covered_skills.update(assessment.keywords_covered)
        
        missing_skills = set(session.role_required_skills) - covered_skills
        
        # Get questions for missing skills with appropriate difficulty
        if missing_skills:
            skill = list(missing_skills)[0]
            # Would call registry to get questions for this skill at this difficulty
            # For now, returning example structure
            questions = self._get_questions_for_skill_and_difficulty(
                skill, difficulty
            )
        else:
            # All skills covered, get any question at this difficulty
            questions = self._get_questions_by_difficulty(difficulty)
        
        # Return first available question (or random from pool)
        if questions:
            return questions[0]
        
        return None
    
    def _calculate_recent_performance(self, session: InterviewSession) -> float:
        """Calculate candidate's recent performance score"""
        if not session.assessments:
            return 0.5  # Neutral if no assessments yet
        
        # Look at last 3 assessments
        recent = session.assessments[-3:]
        
        score_map = {
            ScoreLevel.POOR: 0.2,
            ScoreLevel.FAIR: 0.4,
            ScoreLevel.GOOD: 0.6,
            ScoreLevel.EXCELLENT: 0.8,
            ScoreLevel.OUTSTANDING: 1.0,
        }
        
        scores = [score_map.get(a.score_level, 0.5) for a in recent]
        return sum(scores) / len(scores) if scores else 0.5
    
    def _determine_next_difficulty(self, performance: float, current: str) -> str:
        """Determine next question difficulty"""
        
        if current == "easy":
            if performance > self.difficulty_thresholds["easy_to_medium"]:
                return "medium"
            return "easy"
        
        elif current == "medium":
            if performance > self.difficulty_thresholds["medium_to_hard"]:
                return "hard"
            elif performance < self.difficulty_thresholds["downgrade_threshold"]:
                return "easy"
            return "medium"
        
        elif current == "hard":
            if performance > self.difficulty_thresholds["hard_to_expert"]:
                return "expert" if self._has_expert_questions() else "hard"
            elif performance < self.difficulty_thresholds["downgrade_threshold"]:
                return "medium"
            return "hard"
        
        return current
    
    def _has_expert_questions(self) -> bool:
        """Check if registry has expert-level questions"""
        # Would check registry - for now assume true
        return True
    
    def _get_questions_for_skill_and_difficulty(self, skill: str, difficulty: str) -> list[Question]:
        """Get questions for a specific skill at difficulty level"""
        # Would query registry
        # For now returning empty list
        return []
    
    def _get_questions_by_difficulty(self, difficulty: str) -> list[Question]:
        """Get questions at specific difficulty level"""
        # Would query registry
        # For now returning empty list
        return []
    
    def _adapt_difficulty(self, session: InterviewSession) -> None:
        """Update difficulty for next question based on performance"""
        # Called after each answer to adjust upcoming question difficulty
        recent = self._calculate_recent_performance(session)
        new_difficulty = self._determine_next_difficulty(recent, session.current_difficulty)
        session.current_difficulty = new_difficulty
    
    def get_session_status(self, session_id: str) -> dict:
        """Get status of interview session"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "candidate_id": session.candidate_id,
            "progress": f"{session.current_question_index}/{session.total_questions}",
            "current_difficulty": session.current_difficulty,
            "is_complete": session.is_complete,
            "questions_asked": len(session.questions_asked),
            "avg_score": self._calculate_recent_performance(session),
        }
    
    def end_session(self, session_id: str) -> dict:
        """End interview session"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        session.is_complete = True
        
        # Return session summary
        performance = self._calculate_recent_performance(session)
        
        return {
            "session_id": session_id,
            "total_questions": len(session.questions_asked),
            "total_assessments": len(session.assessments),
            "overall_performance": performance,
            "final_difficulty": session.current_difficulty,
        }
