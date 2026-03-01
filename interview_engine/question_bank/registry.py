from collections import defaultdict
from .technical import TECHNICAL_QUESTIONS
from .behavioral import BEHAVIORAL_QUESTIONS
from .situational import SITUATIONAL_QUESTIONS
from .culture import CULTURE_QUESTIONS
from .models import Question

ALL_QUESTIONS: list[Question] = (
    TECHNICAL_QUESTIONS +
    BEHAVIORAL_QUESTIONS +
    SITUATIONAL_QUESTIONS +
    CULTURE_QUESTIONS
)

# Indexed lookup for fast filtering
INDEX_BY_DOMAIN: dict[str, list[Question]] = defaultdict(list)
INDEX_BY_CATEGORY: dict[str, list[Question]] = defaultdict(list)
INDEX_BY_DIFFICULTY: dict[str, list[Question]] = defaultdict(list)

for q in ALL_QUESTIONS:
    INDEX_BY_DOMAIN[q.domain].append(q)
    INDEX_BY_CATEGORY[q.category].append(q)
    INDEX_BY_DIFFICULTY[q.difficulty].append(q)