from .registry import (
    INDEX_BY_DOMAIN,
    INDEX_BY_CATEGORY,
    INDEX_BY_DIFFICULTY,
    ALL_QUESTIONS
)
from .skill_aliases import ALIASES

def normalise_skill(skill: str) -> str:
    key = skill.lower().strip()
    return ALIASES.get(key, key.replace(" ", "_"))

def get_questions(
    domain: str | None = None,
    category: str | None = None,
    difficulty: str | None = None,
) -> list:
    pool = ALL_QUESTIONS

    if domain:
        domain = normalise_skill(domain)
        pool = INDEX_BY_DOMAIN.get(domain, [])

    if category:
        pool = [q for q in pool if q.category == category]

    if difficulty:
        pool = [q for q in pool if q.difficulty == difficulty]

    return pool


# ===========================
# ADVANCED FEATURES
# ===========================
# These modules extend the base question_bank with advanced capabilities
# without modifying the core source code

try:
    from .assessor import (
        AnswerAssessment,
        AnswerAssessor,
        ScoreLevel,
    )
    ASSESSOR_AVAILABLE = True
except ImportError:
    ASSESSOR_AVAILABLE = False

try:
    from .evaluator import (
        CandidateEvaluation,
        CandidateEvaluator,
        CandidateRating,
        SkillAssessment,
    )
    EVALUATOR_AVAILABLE = True
except ImportError:
    EVALUATOR_AVAILABLE = False

try:
    from .adaptive_engine import (
        AdaptiveInterviewEngine,
        InterviewSession,
    )
    ADAPTIVE_ENGINE_AVAILABLE = True
except ImportError:
    ADAPTIVE_ENGINE_AVAILABLE = False

try:
    from .analytics import (
        InterviewAnalytics,
        InterviewMetrics,
        ComparisonMetrics,
    )
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False

try:
    from .ai_features import (
        IntelligentQuestionSelector,
        PerformanceAnalyzer,
        QuestionRecommendation,
    )
    AI_FEATURES_AVAILABLE = True
except ImportError:
    AI_FEATURES_AVAILABLE = False


# Convenience function for getting advanced capabilities
def get_advanced_features() -> dict:
    """Get status of all advanced features"""
    return {
        "answer_assessment": ASSESSOR_AVAILABLE,
        "candidate_evaluation": EVALUATOR_AVAILABLE,
        "adaptive_interviewing": ADAPTIVE_ENGINE_AVAILABLE,
        "interview_analytics": ANALYTICS_AVAILABLE,
        "ai_question_selection": AI_FEATURES_AVAILABLE,
    }