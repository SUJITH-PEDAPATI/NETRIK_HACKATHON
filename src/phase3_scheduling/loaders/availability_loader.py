"""
phase3_scheduling/loaders/availability_loader.py
─────────────────────────────────────────────────
Advanced data loader with multiple format support and transformation.
"""

import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# Sample template for JSON data format
SAMPLE_JSON_TEMPLATE = {
    "candidates": [
        {
            "id": "C001",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "preferred_times": ["09:00-12:00", "14:00-17:00"],
            "unavailable_dates": [],
            "skills": ["Python", "AWS"],
            "rounds_needed": 2,
        }
    ],
    "interviewers": [
        {
            "id": "I001",
            "name": "John Smith",
            "email": "john@example.com",
            "available_times": ["09:00-12:00", "14:00-17:00"],
            "unavailable_dates": [],
            "specialties": ["Python", "Backend"],
            "max_per_day": 3,
        }
    ],
    "date_range": {
        "start_date": "2026-03-10",
        "end_date": "2026-03-15",
    },
}


def generate_random(
    num_candidates: int = 5,
    num_interviewers: int = 3,
    days: int = 5,
) -> Dict:
    """
    Generate random candidate and interviewer data for testing.
    
    Args:
        num_candidates: Number of candidates
        num_interviewers: Number of interviewers
        days: Number of days to schedule over
        
    Returns:
        Dictionary with candidates, interviewers, and date range
    """
    import random
    
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    candidates = []
    interviewers = []
    
    skills = ["Python", "AWS", "Java", "React", "System Design", "Data Science"]
    
    for i in range(num_candidates):
        candidates.append({
            "id": f"C{i+1:03d}",
            "name": f"Candidate {i+1}",
            "email": f"cand{i+1}@example.com",
            "preferred_times": [f"{9+j}:00-{10+j}:00" for j in range(6)],
            "unavailable_dates": [],
            "skills": random.sample(skills, k=random.randint(1, 3)),
            "rounds_needed": random.randint(1, 3),
            "seniority": random.choice(["junior", "mid", "senior"]),
        })
    
    for i in range(num_interviewers):
        interviewers.append({
            "id": f"I{i+1:03d}",
            "name": f"Interviewer {i+1}",
            "email": f"int{i+1}@example.com",
            "available_times": [f"{9+j}:00-{10+j}:00" for j in range(8)],
            "unavailable_dates": [],
            "specialties": random.sample(skills, k=random.randint(2, 4)),
            "max_per_day": random.randint(2, 4),
            "rounds": random.sample(["technical", "behavioral", "cultural"], k=random.randint(1, 3)),
        })
    
    return {
        "candidates": candidates,
        "interviewers": interviewers,
        "date_range": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": (start_date + timedelta(days=days)).strftime("%Y-%m-%d"),
        },
    }


def load_from_json(filepath: str) -> Dict:
    """Load data from JSON file."""
    logger.info(f"Loading data from JSON: {filepath}")
    with open(filepath, 'r') as f:
        data = json.load(f)
    logger.info(f"Loaded {len(data['candidates'])} candidates, {len(data['interviewers'])} interviewers")
    return data


def load_from_csv(candidates_file: str, interviewers_file: str, dates_file: Optional[str] = None) -> Dict:
    """Load data from CSV files."""
    logger.info(f"Loading candidates from: {candidates_file}")
    candidates = []
    with open(candidates_file, 'r') as f:
        reader = csv.DictReader(f)
        candidates = list(reader)
    
    logger.info(f"Loading interviewers from: {interviewers_file}")
    interviewers = []
    with open(interviewers_file, 'r') as f:
        reader = csv.DictReader(f)
        interviewers = list(reader)
    
    date_range = {
        "start_date": (datetime.now()).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
    }
    
    if dates_file:
        with open(dates_file, 'r') as f:
            reader = csv.DictReader(f)
            dates_data = list(reader)[0]
            date_range = {
                "start_date": dates_data.get("start_date"),
                "end_date": dates_data.get("end_date"),
            }
    
    logger.info(f"Loaded {len(candidates)} candidates, {len(interviewers)} interviewers")
    return {
        "candidates": candidates,
        "interviewers": interviewers,
        "date_range": date_range,
    }


def load_from_pipeline_results(
    ranked_results: List[Dict],
    interviewers_data: Dict,
    days: int = 5,
    start_date: Optional[str] = None,
) -> Dict:
    """
    Transform Phase 1-2 pipeline results into scheduling format.
    
    Args:
        ranked_results: Ranked candidate results from Phase 1-2
        interviewers_data: Interviewer availability data
        days: Number of days to schedule
        start_date: Start date for scheduling
        
    Returns:
        Formatted data for Phase 3
    """
    logger.info(f"Bridging {len(ranked_results)} candidates from pipeline")
    
    if start_date is None:
        start_date = (datetime.now()).strftime("%Y-%m-%d")
    
    candidates = []
    for result in ranked_results:
        cand = {
            "id": result.get("id", f"C{len(candidates)+1:03d}"),
            "name": result.get("name", "Unknown"),
            "email": result.get("email", ""),
            "match_score": result.get("score", 0),
            "preferred_times": ["09:00-12:00", "14:00-17:00"],
            "unavailable_dates": [],
            "skills": result.get("skills", []),
            "rounds_needed": result.get("rounds_needed", 2),
            "seniority": result.get("seniority", "mid"),
        }
        candidates.append(cand)
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    
    return {
        "candidates": candidates,
        "interviewers": interviewers_data,
        "date_range": {
            "start_date": start_date,
            "end_date": (start_dt + timedelta(days=days)).strftime("%Y-%m-%d"),
        },
    }


def validate_data(data: Dict) -> tuple[bool, List[str]]:
    """
    Validate data structure and content.
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    if "candidates" not in data or not data["candidates"]:
        errors.append("Missing or empty candidates list")
    
    if "interviewers" not in data or not data["interviewers"]:
        errors.append("Missing or empty interviewers list")
    
    if "date_range" not in data:
        errors.append("Missing date_range")
    
    for cand in data.get("candidates", []):
        if not cand.get("id") or not cand.get("name"):
            errors.append(f"Invalid candidate: missing id or name")
    
    for inter in data.get("interviewers", []):
        if not inter.get("id") or not inter.get("name"):
            errors.append(f"Invalid interviewer: missing id or name")
    
    return len(errors) == 0, errors


class AvailabilityLoader(ABC):
    """Abstract base class for availability loaders."""
    
    def __init__(self):
        """Initialize loader."""
        logger.info(f"Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def load(self, source: str) -> Dict:
        """
        Load availability data.
        
        Args:
            source: Source path or connection string
            
        Returns:
            Dictionary with candidates and interviewers
        """
        pass
    
    def validate(self, data: Dict) -> bool:
        """Validate loaded data structure."""
        raise NotImplementedError()
