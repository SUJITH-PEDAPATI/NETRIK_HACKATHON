"""
Technical interview questions
"""

from typing import List, Dict, Any
from .models import Question, QuestionType, DifficultyLevel


class TechnicalQuestions:
    """Repository of technical interview questions"""
    
    PYTHON_QUESTIONS: List[Question] = [
        Question(
            id="tech_py_001",
            question_text="Explain the difference between list comprehension and generator expressions in Python.",
            question_type=QuestionType.TECHNICAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["Python", "Performance"],
            keywords=["list comprehension", "generator", "memory", "lazy evaluation"],
            ideal_answer="List comprehensions create an entire list in memory, while generator expressions yield values one at a time using lazy evaluation, saving memory for large datasets.",
            follow_ups=[
                "When would you prefer one over the other?",
                "What's the performance difference on large datasets?"
            ]
        ),
        Question(
            id="tech_py_002",
            question_text="What are decorators in Python and provide a practical example.",
            question_type=QuestionType.TECHNICAL,
            difficulty=DifficultyLevel.HARD,
            skills=["Python", "Design Patterns"],
            keywords=["decorators", "functions", "closures"],
            ideal_answer="Decorators are functions that modify other functions or classes. They use closures to wrap a function and extend its behavior without modifying it.",
            follow_ups=[
                "How would you implement a timing decorator?",
                "Can you stack multiple decorators?"
            ]
        ),
    ]
    
    AWS_QUESTIONS: List[Question] = [
        Question(
            id="tech_aws_001",
            question_text="Explain the differences between EC2, Lambda, and ECS in AWS.",
            question_type=QuestionType.TECHNICAL,
            difficulty=DifficultyLevel.MEDIUM,
            skills=["AWS", "Cloud Infrastructure"],
            keywords=["EC2", "Lambda", "ECS", "serverless", "containers"],
            ideal_answer="EC2 provides virtual machines with full control, Lambda is serverless for short tasks, ECS runs Docker containers. EC2 needs management, Lambda auto-scales, ECS bridges them.",
            follow_ups=[
                "When would you choose one over the others?",
                "What about cost implications?"
            ]
        ),
        Question(
            id="tech_aws_002",
            question_text="How would you design a highly available architecture on AWS?",
            question_type=QuestionType.TECHNICAL,
            difficulty=DifficultyLevel.HARD,
            skills=["AWS", "System Design", "DevOps"],
            keywords=["high availability", "multi-AZ", "load balancer", "failover"],
            ideal_answer="Use multi-AZ deployment, load balancers, auto-scaling groups, RDS Multi-AZ for database, and CloudFront for caching.",
            follow_ups=[
                "How would you handle database failover?",
                "What about disaster recovery across regions?"
            ]
        ),
    ]
    
    SYSTEM_DESIGN_QUESTIONS: List[Question] = [
        Question(
            id="tech_sd_001",
            question_text="Design a URL shortening service (like TinyURL).",
            question_type=QuestionType.TECHNICAL,
            difficulty=DifficultyLevel.HARD,
            skills=["System Design", "Backend"],
            keywords=["scalability", "database", "caching", "distribution"],
            ideal_answer="Use base62 encoding for short codes, store mappings in database, cache with Redis, use CDN for distribution, partition data by short code prefix.",
            follow_ups=[
                "How would you handle traffic spikes?",
                "What about analytics/tracking?"
            ]
        ),
    ]
    
    @classmethod
    def get_all_questions(cls) -> List[Question]:
        """Get all technical questions"""
        return cls.PYTHON_QUESTIONS + cls.AWS_QUESTIONS + cls.SYSTEM_DESIGN_QUESTIONS
    
    @classmethod
    def get_questions_by_skill(cls, skill: str) -> List[Question]:
        """Get technical questions for a specific skill"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if skill.lower() in [s.lower() for s in q.skills]]
    
    @classmethod
    def get_questions_by_difficulty(cls, difficulty: DifficultyLevel) -> List[Question]:
        """Get questions by difficulty level"""
        all_questions = cls.get_all_questions()
        return [q for q in all_questions if q.difficulty == difficulty]
    
    @classmethod
    def add_question(cls, question: Question) -> None:
        """Add a new technical question"""
        # This would typically save to a database
        # For now, we're demonstrating the method
        cls.get_all_questions().append(question)
