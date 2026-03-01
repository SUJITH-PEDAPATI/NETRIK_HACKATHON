"""
Behavioral interview questions
"""

from typing import List
from .models import Question, QuestionType, DifficultyLevel


class BehavioralQuestions:
    """Repository of behavioral interview questions"""
    
    LEADERSHIP_QUESTIONS: List[Question] = [
        Question(
            id="behav_lead_001",
            question_text="Tell me about a time when you had to lead a team through a difficult project.",
            question_type=QuestionType.BEHAVIORAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Leadership", "Communication"],
            keywords=["leadership", "team", "challenge", "outcome"],
            ideal_answer="Look for: specific situation, actions taken, how team was motivated, positive outcome achieved.",
            follow_ups=[
                "What would you do differently?",
                "How did the team respond?"
            ]
        ),
        Question(
            id="behav_lead_002",
            question_text="Describe a situation where you had to make a difficult decision with incomplete information.",
            question_type=QuestionType.BEHAVIORAL,
            difficulty=DifficultyLevel.HARD,
            skills=["Decision Making", "Leadership"],
            keywords=["decision", "uncertainty", "risk", "outcome"],
            ideal_answer="Look for: problem understanding, information gathering, decision rationale, results and reflection.",
            follow_ups=[
                "How did you validate your decision?",
                "Would you make the same choice again?"
            ]
        ),
    ]
    
    TEAMWORK_QUESTIONS: List[Question] = [
        Question(
            id="behav_team_001",
            question_text="Tell me about a time you had to work with someone you didn't get along with.",
            question_type=QuestionType.BEHAVIORAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Teamwork", "Communication"],
            keywords=["conflict", "collaboration", "communication", "resolution"],
            ideal_answer="Look for: understanding of different perspectives, effort to cooperate, mature handling of conflict.",
            follow_ups=[
                "What did you learn?",
                "How would you handle it now?"
            ]
        ),
        Question(
            id="behav_team_002",
            question_text="Describe a time when you helped a teammate succeed, even though it wasn't your responsibility.",
            question_type=QuestionType.BEHAVIORAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Teamwork", "Empathy"],
            keywords=["support", "collaboration", "initiative", "helping"],
            ideal_answer="Look for: initiative, empathy, willingness to help beyond scope, positive team impact.",
            follow_ups=[
                "What was the outcome?",
                "Do you often take on extra work?"
            ]
        ),
    ]
    
    CONFLICT_RESOLUTION_QUESTIONS: List[Question] = [
        Question(
            id="behav_conf_001",
            question_text="Tell me about a time when you had to deal with a conflict with your manager.",
            question_type=QuestionType.BEHAVIORAL,
            difficulty=DifficultyLevel.HARD,
            skills=["Conflict Resolution", "Communication"],
            keywords=["conflict", "manager", "hierarchy", "resolution", "respect"],
            ideal_answer="Look for: respect for hierarchy, clear communication, mature problem-solving, professional tone.",
            follow_ups=[
                "How was it resolved?",
                "Did your relationship improve?"
            ]
        ),
    ]
    
    @classmethod
    def get_all_questions(cls) -> List[Question]:
        """Get all behavioral questions"""
        return cls.LEADERSHIP_QUESTIONS + cls.TEAMWORK_QUESTIONS + cls.CONFLICT_RESOLUTION_QUESTIONS
    
    @classmethod
    def get_questions_by_skill(cls, skill: str) -> List[Question]:
        """Get behavioral questions for a specific skill"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if skill.lower() in [s.lower() for s in q.skills]]
    
    @classmethod
    def get_questions_by_difficulty(cls, difficulty: DifficultyLevel) -> List[Question]:
        """Get questions by difficulty level"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if q.difficulty == difficulty]
