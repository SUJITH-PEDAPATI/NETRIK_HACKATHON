"""
Data models for interview questions and interview sets
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class QuestionType(Enum):
    """Types of interview questions"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    CULTURE = "culture"


class DifficultyLevel(Enum):
    """Difficulty levels for questions"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class Question:
    """
    Represents a single interview question
    
    Attributes:
        id: Unique identifier for the question
        question_text: The actual question to ask
        question_type: Type of question (technical, behavioral, etc.)
        difficulty: Difficulty level
        skills: List of skills this question tests
        keywords: Keywords related to the question
        ideal_answer: Sample/ideal answer
        follow_ups: Optional follow-up questions
        metadata: Additional metadata
    """
    id: str
    question_text: str
    question_type: QuestionType
    difficulty: DifficultyLevel
    skills: List[str]
    keywords: List[str] = field(default_factory=list)
    ideal_answer: Optional[str] = None
    follow_ups: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert question to dictionary"""
        return {
            "id": self.id,
            "question_text": self.question_text,
            "question_type": self.question_type.value,
            "difficulty": self.difficulty.value,
            "skills": self.skills,
            "keywords": self.keywords,
            "ideal_answer": self.ideal_answer,
            "follow_ups": self.follow_ups,
            "metadata": self.metadata
        }


@dataclass
class InterviewSet:
    """
    Represents a curated set of interview questions for a specific role
    
    Attributes:
        role: Job role/title
        required_skills: Skills required for the role
        questions: List of questions selected for this interview
        duration_minutes: Estimated interview duration
        description: Description of the interview
        metadata: Additional metadata
    """
    role: str
    required_skills: List[str]
    questions: List[Question]
    duration_minutes: int = 60
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_questions_by_type(self, question_type: QuestionType) -> List[Question]:
        """Get questions filtered by type"""
        return [q for q in self.questions if q.question_type == question_type]
    
    def get_questions_by_skill(self, skill: str) -> List[Question]:
        """Get questions filtered by skill"""
        return [q for q in self.questions if skill.lower() in [s.lower() for s in q.skills]]
    
    def get_questions_by_difficulty(self, difficulty: DifficultyLevel) -> List[Question]:
        """Get questions filtered by difficulty"""
        return [q for q in self.questions if q.difficulty == difficulty]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert interview set to dictionary"""
        return {
            "role": self.role,
            "required_skills": self.required_skills,
            "questions": [q.to_dict() for q in self.questions],
            "duration_minutes": self.duration_minutes,
            "description": self.description,
            "metadata": self.metadata
        }
