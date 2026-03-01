"""
Culture and fit interview questions
"""

from typing import List
from .models import Question, QuestionType, DifficultyLevel


class CultureQuestions:
    """Repository of culture and values-based interview questions"""
    
    VALUES_ALIGNMENT_QUESTIONS: List[Question] = [
        Question(
            id="cult_val_001",
            question_text="What personal values are most important to you in your career?",
            question_type=QuestionType.CULTURE,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Self-Awareness", "Values"],
            keywords=["values", "purpose", "fulfillment", "career"],
            ideal_answer="Look for thoughtful reflection, alignment with company values, introspection, authenticity.",
            follow_ups=[
                "How do these values guide your decisions?",
                "What compromises would be deal-breakers?"
            ]
        ),
        Question(
            id="cult_val_002",
            question_text="Tell me about your ideal work environment and company culture.",
            question_type=QuestionType.CULTURE,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Self-Awareness", "Communication"],
            keywords=["culture", "environment", "team", "growth"],
            ideal_answer="Look for specific needs, self-knowledge, alignment with company culture, realistic expectations.",
            follow_ups=[
                "Why is that important to you?",
                "What would make you leave a job?"
            ]
        ),
    ]
    
    COLLABORATION_QUESTIONS: List[Question] = [
        Question(
            id="cult_collab_001",
            question_text="How do you contribute to a positive team culture?",
            question_type=QuestionType.CULTURE,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Teamwork", "Culture"],
            keywords=["culture", "community", "support", "belonging"],
            ideal_answer="Look for proactive contributions, empathy, inclusiveness, mentoring others.",
            follow_ups=[
                "Can you give a specific example?",
                "What behaviors undermine culture?"
            ]
        ),
    ]
    
    DIVERSITY_INCLUSION_QUESTIONS: List[Question] = [
        Question(
            id="cult_div_001",
            question_text="How do you approach working with people from diverse backgrounds?",
            question_type=QuestionType.CULTURE,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Diversity", "Inclusion"],
            keywords=["diversity", "inclusion", "perspective", "respect"],
            ideal_answer="Look for genuine curiosity, respect, willingness to learn, avoiding stereotypes.",
            follow_ups=[
                "Tell me about a time you worked with someone very different from you.",
                "How do you handle different communication styles?"
            ]
        ),
    ]
    
    GROWTH_LEARNING_QUESTIONS: List[Question] = [
        Question(
            id="cult_growth_001",
            question_text="What does continuous learning mean to you, and how do you practice it?",
            question_type=QuestionType.CULTURE,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Learning", "Growth Mindset"],
            keywords=["learning", "development", "growth", "curiosity"],
            ideal_answer="Look for specific practices, humility, curiosity, investment in growth.",
            follow_ups=[
                "What's something you recently learned?",
                "How do you handle failure in learning?"
            ]
        ),
        Question(
            id="cult_growth_002",
            question_text="How do you handle feedback and criticism?",
            question_type=QuestionType.CULTURE,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Growth Mindset", "Resilience"],
            keywords=["feedback", "growth", "criticism", "reflection"],
            ideal_answer="Look for openness, reflection, growth orientation, not being defensive.",
            follow_ups=[
                "Tell me about challenging feedback you received.",
                "How did you respond?"
            ]
        ),
    ]
    
    @classmethod
    def get_all_questions(cls) -> List[Question]:
        """Get all culture questions"""
        return (cls.VALUES_ALIGNMENT_QUESTIONS + cls.COLLABORATION_QUESTIONS + 
                cls.DIVERSITY_INCLUSION_QUESTIONS + cls.GROWTH_LEARNING_QUESTIONS)
    
    @classmethod
    def get_questions_by_skill(cls, skill: str) -> List[Question]:
        """Get culture questions for a specific skill"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if skill.lower() in [s.lower() for s in q.skills]]
    
    @classmethod
    def get_questions_by_difficulty(cls, difficulty: DifficultyLevel) -> List[Question]:
        """Get questions by difficulty level"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if q.difficulty == difficulty]
