"""
Skill aliases and normalization for consistent skill matching
"""

from typing import Dict, List, Optional, Set


class SkillAliases:
    """Maps skill aliases to canonical skill names"""
    
    # Canonical skill names with their common aliases
    SKILL_ALIASES: Dict[str, Set[str]] = {
        "Python": {"py", "python3", "python 3", "python"},
        "JavaScript": {"js", "javascript", "node", "nodejs", "node.js"},
        "Java": {"java", "jvm"},
        "C++": {"c++", "cpp", "c plus plus"},
        "C#": {"c#", "csharp", "c sharp"},
        "Go": {"golang", "go"},
        "Rust": {"rust", "rs"},
        "TypeScript": {"typescript", "ts", "tsx"},
        
        # Web Frameworks
        "React": {"react", "reactjs", "react.js"},
        "Vue": {"vue", "vuejs", "vue.js"},
        "Angular": {"angular", "angularjs"},
        "Django": {"django"},
        "Flask": {"flask"},
        "FastAPI": {"fastapi", "fast api"},
        "Node.js": {"nodejs", "node", "node.js"},
        "Express": {"express", "expressjs"},
        
        # Cloud Platforms
        "AWS": {"aws", "amazon web services", "amazon aws"},
        "Azure": {"azure", "microsoft azure"},
        "GCP": {"gcp", "google cloud", "google cloud platform"},
        "Kubernetes": {"kubernetes", "k8s", "k3s"},
        "Docker": {"docker", "containerization"},
        
        # Databases
        "SQL": {"sql", "relational database"},
        "PostgreSQL": {"postgresql", "postgres", "psql"},
        "MySQL": {"mysql"},
        "MongoDB": {"mongodb", "mongo"},
        "Redis": {"redis", "cache"},
        "Elasticsearch": {"elasticsearch", "elastic"},
        "DynamoDB": {"dynamodb", "dynamo"},
        
        # Machine Learning
        "Machine Learning": {"ml", "machine learning", "artificial intelligence", "ai"},
        "TensorFlow": {"tensorflow", "tf"},
        "PyTorch": {"pytorch", "torch"},
        "Scikit-learn": {"scikit-learn", "sklearn", "scikit learn"},
        "Pandas": {"pandas", "pd"},
        "NumPy": {"numpy", "np"},
        
        # DevOps & Tools
        "CI/CD": {"ci/cd", "cicd", "continuous integration", "continuous deployment"},
        "Git": {"git", "github", "gitlab", "gitops"},
        "Jenkins": {"jenkins"},
        "GitLab": {"gitlab"},
        "GitHub": {"github"},
        "Docker": {"docker"},
        "Terraform": {"terraform"},
        "Ansible": {"ansible"},
        "Nginx": {"nginx", "apache"},
        "Linux": {"linux", "unix"},
        
        # Data & Analytics
        "SQL": {"sql", "database"},
        "Spark": {"spark", "apache spark"},
        "Hadoop": {"hadoop"},
        "Hive": {"hive", "apache hive"},
        "BigQuery": {"bigquery", "big query"},
        
        # Soft Skills
        "Communication": {"communication", "public speaking", "presentation"},
        "Leadership": {"leadership", "management", "team lead"},
        "Problem Solving": {"problem solving", "problem-solving", "analytical"},
        "Teamwork": {"teamwork", "collaboration", "team player"},
        "Project Management": {"project management", "pm", "agile", "scrum"},
        "Adaptability": {"adaptability", "flexibility", "learning agility"},
        
        # Testing & QA
        "Testing": {"testing", "qa", "quality assurance"},
        "Unit Testing": {"unit testing", "pytest", "unittest", "jest"},
        "Integration Testing": {"integration testing"},
        "Selenium": {"selenium", "automation testing"},
        
        # Mobile Development
        "iOS": {"ios", "swift", "objective-c", "xcode"},
        "Android": {"android", "kotlin", "java"},
        "React Native": {"react native", "react-native"},
        "Flutter": {"flutter"},
        
        # Architecture & Design
        "System Design": {"system design", "architecture", "microservices"},
        "RESTful APIs": {"restful", "rest api", "rest", "api design"},
        "GraphQL": {"graphql", "graph ql"},
        "Design Patterns": {"design patterns", "oop", "object-oriented"},
        "SOLID Principles": {"solid", "solid principles"},
    }
    
    @classmethod
    def normalize_skill(cls, skill: str) -> Optional[str]:
        """
        Normalize a skill name to its canonical form
        
        Args:
            skill: Raw skill name (from resume or job description)
        
        Returns:
            Canonical skill name or None if not found
        """
        skill = skill.strip().lower()
        
        # Direct match (skill is already canonical)
        if skill in cls.SKILL_ALIASES:
            return skill
        
        # Search in aliases
        for canonical, aliases in cls.SKILL_ALIASES.items():
            if skill in aliases or skill == canonical.lower():
                return canonical
        
        # No match found
        return None
    
    @classmethod
    def get_canonical_name(cls, skill: str) -> str:
        """
        Get canonical name for a skill, or return original if not found
        
        Args:
            skill: Raw skill name
        
        Returns:
            Canonical skill name or original skill if no mapping exists
        """
        normalized = cls.normalize_skill(skill)
        return normalized if normalized else skill
    
    @classmethod
    def normalize_skills(cls, skills: List[str]) -> List[str]:
        """
        Normalize a list of skills to canonical names
        
        Args:
            skills: List of raw skill names
        
        Returns:
            List of canonical skill names (deduplicated)
        """
        canonical_skills = set()
        for skill in skills:
            normalized = cls.normalize_skill(skill)
            if normalized:
                canonical_skills.add(normalized)
        
        return sorted(list(canonical_skills))
    
    @classmethod
    def find_similar_skills(cls, skill: str) -> List[str]:
        """
        Find skills similar to the given skill
        
        Args:
            skill: Raw skill name
        
        Returns:
            List of similar canonical skill names
        """
        skill = skill.strip().lower()
        similar = []
        
        for canonical, aliases in cls.SKILL_ALIASES.items():
            # Check for partial matches
            if skill in canonical.lower() or canonical.lower() in skill:
                similar.append(canonical)
            elif skill in aliases or any(alias.startswith(skill[:3]) for alias in aliases):
                similar.append(canonical)
        
        return similar
    
    @classmethod
    def get_all_canonical_skills(cls) -> List[str]:
        """Get list of all canonical skill names"""
        return sorted(list(cls.SKILL_ALIASES.keys()))
    
    @classmethod
    def get_skill_category(cls, skill: str) -> Optional[str]:
        """
        Get category for a skill
        
        Args:
            skill: Canonical skill name
        
        Returns:
            Skill category or None
        """
        canonical = cls.normalize_skill(skill) or skill
        
        # Define categories
        categories = {
            "Programming Languages": ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript"],
            "Web Frameworks": ["React", "Vue", "Angular", "Django", "Flask", "FastAPI", "Node.js", "Express"],
            "Cloud Platforms": ["AWS", "Azure", "GCP", "Kubernetes", "Docker"],
            "Databases": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "DynamoDB"],
            "Machine Learning": ["Machine Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"],
            "DevOps & Tools": ["CI/CD", "Git", "Jenkins", "GitLab", "GitHub", "Docker", "Terraform", "Ansible", "Nginx", "Linux"],
            "Data & Analytics": ["SQL", "Spark", "Hadoop", "Hive", "BigQuery"],
            "Soft Skills": ["Communication", "Leadership", "Problem Solving", "Teamwork", "Project Management", "Adaptability"],
            "Testing & QA": ["Testing", "Unit Testing", "Integration Testing", "Selenium"],
            "Mobile Development": ["iOS", "Android", "React Native", "Flutter"],
            "Architecture & Design": ["System Design", "RESTful APIs", "GraphQL", "Design Patterns", "SOLID Principles"],
        }
        
        for category, skills in categories.items():
            if canonical in skills:
                return category
        
        return None
    
    @classmethod
    def add_skill_alias(cls, canonical_skill: str, alias: str) -> None:
        """
        Add a new skill alias
        
        Args:
            canonical_skill: The canonical skill name
            alias: The alias to add
        """
        if canonical_skill not in cls.SKILL_ALIASES:
            cls.SKILL_ALIASES[canonical_skill] = set()
        
        cls.SKILL_ALIASES[canonical_skill].add(alias.lower())
