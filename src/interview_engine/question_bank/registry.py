"""
Central registry for managing all interview questions across categories
"""

from typing import List, Dict, Optional
import random
from .models import Question, QuestionType, DifficultyLevel, InterviewSet
from .technical import TechnicalQuestions
from .behavioral import BehavioralQuestions
from .situational import SituationalQuestions
from .culture import CultureQuestions


class QuestionRegistry:
    """Central registry for all interview questions"""
    
    def __init__(self):
        """Initialize the registry with all question sources"""
        self._technical_questions = TechnicalQuestions.get_all_questions()
        self._behavioral_questions = BehavioralQuestions.get_all_questions()
        self._situational_questions = SituationalQuestions.get_all_questions()
        self._culture_questions = CultureQuestions.get_all_questions()
        
        # Build index for quick lookups
        self._question_by_id: Dict[str, Question] = {}
        self._build_index()
    
    def _build_index(self) -> None:
        """Build internal index for fast lookups"""
        for question in self.get_all_questions():
            self._question_by_id[question.id] = question
    
    def get_all_questions(self) -> List[Question]:
        """Get all questions in the registry"""
        return (self._technical_questions + self._behavioral_questions + 
                self._situational_questions + self._culture_questions)
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Get a specific question by ID"""
        return self._question_by_id.get(question_id)
    
    def get_questions_by_type(self, question_type: QuestionType) -> List[Question]:
        """Get all questions of a specific type"""
        return [q for q in self.get_all_questions() if q.question_type == question_type]
    
    def get_questions_by_skill(self, skill: str) -> List[Question]:
        """Get all questions that test a specific skill"""
        return [q for q in self.get_all_questions() if skill.lower() in [s.lower() for s in q.skills]]
    
    def get_questions_by_difficulty(self, difficulty: DifficultyLevel) -> List[Question]:
        """Get all questions of a specific difficulty"""
        return [q for q in self.get_all_questions() if q.difficulty == difficulty]
    
    def get_questions_by_type_and_difficulty(self, 
                                             question_type: QuestionType,
                                             difficulty: DifficultyLevel) -> List[Question]:
        """Get questions filtered by both type and difficulty"""
        return [q for q in self.get_all_questions() 
                if q.question_type == question_type and q.difficulty == difficulty]
    
    def get_random_questions(self, count: int, 
                            question_type: Optional[QuestionType] = None,
                            difficulty: Optional[DifficultyLevel] = None) -> List[Question]:
        """Get random questions with optional filtering"""
        questions = self.get_all_questions()
        
        if question_type:
            questions = [q for q in questions if q.question_type == question_type]
        
        if difficulty:
            questions = [q for q in questions if q.difficulty == difficulty]
        
        return random.sample(questions, min(count, len(questions)))
    
    def create_interview_set(self, 
                            role: str,
                            required_skills: List[str],
                            total_questions: int = 8,
                            technical_ratio: float = 0.4,
                            behavioral_ratio: float = 0.3,
                            situational_ratio: float = 0.2,
                            culture_ratio: float = 0.1) -> InterviewSet:
        """
        Create a curated interview set for a specific role
        
        Args:
            role: Job title/role
            required_skills: List of required skills for the role
            total_questions: Total number of questions to include
            technical_ratio: Proportion of technical questions (0-1)
            behavioral_ratio: Proportion of behavioral questions (0-1)
            situational_ratio: Proportion of situational questions (0-1)
            culture_ratio: Proportion of culture questions (0-1)
        
        Returns:
            InterviewSet with curated questions
        """
        questions = []
        
        # Calculate number of each type
        num_technical = int(total_questions * technical_ratio)
        num_behavioral = int(total_questions * behavioral_ratio)
        num_situational = int(total_questions * situational_ratio)
        num_culture = int(total_questions * culture_ratio)
        
        # Get questions for required skills (prioritize)
        for skill in required_skills:
            skill_questions = self.get_questions_by_skill(skill)
            for q in skill_questions[:2]:  # Get up to 2 per skill
                if q not in questions:
                    questions.append(q)
        
        # Fill remaining with random questions of each type
        if len(questions) < num_technical + num_technical:
            technical = self.get_random_questions(
                max(0, num_technical - len([q for q in questions if q.question_type == QuestionType.TECHNICAL])),
                question_type=QuestionType.TECHNICAL
            )
            questions.extend(technical)
        
        if len(questions) < total_questions:
            behavioral = self.get_random_questions(
                max(0, num_behavioral - len([q for q in questions if q.question_type == QuestionType.BEHAVIORAL])),
                question_type=QuestionType.BEHAVIORAL
            )
            questions.extend(behavioral)
        
        if len(questions) < total_questions:
            situational = self.get_random_questions(
                max(0, num_situational - len([q for q in questions if q.question_type == QuestionType.SITUATIONAL])),
                question_type=QuestionType.SITUATIONAL
            )
            questions.extend(situational)
        
        if len(questions) < total_questions:
            culture = self.get_random_questions(
                max(0, num_culture - len([q for q in questions if q.question_type == QuestionType.CULTURE])),
                question_type=QuestionType.CULTURE
            )
            questions.extend(culture)
        
        # Limit to total_questions
        questions = questions[:total_questions]
        
        return InterviewSet(
            role=role,
            required_skills=required_skills,
            questions=questions,
            duration_minutes=60
        )
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the question registry"""
        all_questions = self.get_all_questions()
        
        stats = {
            "total_questions": len(all_questions),
            "technical": len([q for q in all_questions if q.question_type == QuestionType.TECHNICAL]),
            "behavioral": len([q for q in all_questions if q.question_type == QuestionType.BEHAVIORAL]),
            "situational": len([q for q in all_questions if q.question_type == QuestionType.SITUATIONAL]),
            "culture": len([q for q in all_questions if q.question_type == QuestionType.CULTURE]),
            "easy": len([q for q in all_questions if q.difficulty == DifficultyLevel.EASY]),
            "medium": len([q for q in all_questions if q.difficulty == DifficultyLevel.MEDIUM]),
            "hard": len([q for q in all_questions if q.difficulty == DifficultyLevel.HARD]),
        }
        
        return stats
