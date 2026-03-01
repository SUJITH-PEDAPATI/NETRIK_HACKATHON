"""
Situational interview questions (hypothetical scenarios)
"""

from typing import List
from .models import Question, QuestionType, DifficultyLevel


class SituationalQuestions:
    """Repository of situational interview questions"""
    
    PROBLEM_SOLVING_QUESTIONS: List[Question] = [
        Question(
            id="sit_prob_001",
            question_text="If a critical production system went down at 2 AM, how would you handle it?",
            question_type=QuestionType.SITUATIONAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Problem Solving", "Pressure Management"],
            keywords=["incident", "response", "communication", "documentation"],
            ideal_answer="Immediately assess impact, activate incident response, communicate updates, fix the root cause, document lessons learned.",
            follow_ups=[
                "How would you prevent recurrence?",
                "Would you wake up the team?"
            ]
        ),
        Question(
            id="sit_prob_002",
            question_text="You discover a major bug in production code that you wrote. What do you do?",
            question_type=QuestionType.SITUATIONAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Accountability", "Problem Solving"],
            keywords=["bug", "responsibility", "fix", "communication"],
            ideal_answer="Immediately report it, take ownership, assess impact, create a fix, implement it, communicate timeline.",
            follow_ups=[
                "How would you ensure it doesn't happen again?",
                "Would you be worried about judgment?"
            ]
        ),
    ]
    
    RESOURCE_MANAGEMENT_QUESTIONS: List[Question] = [
        Question(
            id="sit_res_001",
            question_text="You're assigned to a project with half the budget you requested. How do you proceed?",
            question_type=QuestionType.SITUATIONAL,
            difficulty=DifficultyLevel.HARD,
            skills=["Resource Management", "Planning"],
            keywords=["budget", "constraints", "prioritization", "strategy"],
            ideal_answer="Prioritize MVP features, identify risks, be creative with tools/resources, communicate constraints clearly.",
            follow_ups=[
                "How would you manage stakeholder expectations?",
                "Would you request more budget later?"
            ]
        ),
        Question(
            id="sit_res_002",
            question_text="A key team member quits unexpectedly during a critical project. What do you do?",
            question_type=QuestionType.SITUATIONAL,
            difficulty=DifficultyLevel.HARD,
            skills=["Leadership", "Adaptability"],
            keywords=["team change", "continuity", "knowledge transfer", "problem solving"],
            ideal_answer="Document their work immediately, redistribute tasks, possibly bring in help, maintain team morale.",
            follow_ups=[
                "How do you prevent knowledge loss?",
                "What about project timeline?"
            ]
        ),
    ]
    
    ETHICAL_QUESTIONS: List[Question] = [
        Question(
            id="sit_eth_001",
            question_text="Your manager asks you to cut corners on testing to meet a deadline. How do you respond?",
            question_type=QuestionType.SITUATIONAL,
            difficulty=DifficultyLevel.HARD,
            skills=["Ethics", "Communication"],
            keywords=["integrity", "testing", "quality", "deadline"],
            ideal_answer="Respectfully explain risks, propose alternatives (scope reduction, timeline adjustment), escalate if necessary.",
            follow_ups=[
                "What if the manager insists?",
                "Would you compromise on anything?"
            ]
        ),
    ]
    
    @classmethod
    def get_all_questions(cls) -> List[Question]:
        """Get all situational questions"""
        return cls.PROBLEM_SOLVING_QUESTIONS + cls.RESOURCE_MANAGEMENT_QUESTIONS + cls.ETHICAL_QUESTIONS
    
    @classmethod
    def get_questions_by_skill(cls, skill: str) -> List[Question]:
        """Get situational questions for a specific skill"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if skill.lower() in [s.lower() for s in q.skills]]
    
    @classmethod
    def get_questions_by_difficulty(cls, difficulty: DifficultyLevel) -> List[Question]:
        """Get questions by difficulty level"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if q.difficulty == difficulty]
