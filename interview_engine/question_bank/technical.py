from .models import Question

TECHNICAL_QUESTIONS: list[Question] = [

    Question(
        id="py_easy_01",
        domain="python",
        category="technical",
        difficulty="easy",
        text="Explain the difference between a list and a tuple in Python...",
        follow_up="How does immutability affect memory usage?",
        eval_hint="Mutability, hashability, dict/set usage."
    ),

    Question(
        id="ml_hard_02",
        domain="machine_learning",
        category="technical",
        difficulty="hard",
        text="Design a recommendation system for a streaming platform...",
        follow_up="How would you handle cold-start?",
        eval_hint="Two-tower model, A/B testing, serving architecture."
    ),
]