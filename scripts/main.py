"""
Main entry point demonstrating the full HR Automation resume matching pipeline
"""

import logging
from pathlib import Path
from resume_extractor import ResumeParser
from pipeline import ResumeMatcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Complete HR Automation workflow:
    1. Parse all resumes from a folder
    2. Build ANN index for fast retrieval
    3. Match against a job description
    """
    
    # Step 1: Initialize parser and extract all resumes
    parser = ResumeParser(use_ocr=False)  # Set use_ocr=True if you have scanned PDFs
    
    resumes_folder = "path/to/resumes"
    logger.info(f"Parsing resumes from {resumes_folder}...")
    resumes = parser.parse_folder(resumes_folder)
    
    if not resumes:
        logger.error("No resumes found")
        return
    
    logger.info(f"Successfully parsed {len(resumes)} resumes")
    
    # Print sample extracted data
    for i, resume in enumerate(resumes[:2]):
        logger.info(f"\n--- Resume {i+1}: {resume.get('file_path')} ---")
        logger.info(f"Skills: {resume.get('skills', [])}")
        logger.info(f"Experience: {resume.get('experience', [])}")
        logger.info(f"Education: {resume.get('education', [])}")
        logger.info(f"Years of Experience: {resume.get('total_years_exp', 0)}")
    
    # Step 2: Initialize matcher and build index
    matcher = ResumeMatcher()
    logger.info("\nIndexing resumes for fast retrieval...")
    matcher.index_resumes(resumes)
    
    # Step 3: Match against job description
    job_description = \"\"\"
    We are looking for a Senior Software Engineer with expertise in Python and cloud technologies.
    Required skills: Python, AWS, Docker, Kubernetes, CI/CD
    Minimum 5 years of experience in backend development
    Bachelor's degree in Computer Science or related field
    \"\"\\"
    
    job_metadata = {
        "job_title": "Senior Software Engineer",
        "skills": ["Python", "AWS", "Docker", "Kubernetes"],
        "years_experience": 5
    }
    
    logger.info("\nMatching candidates against job description...")
    ranked_candidates = matcher.match_job_description(job_description, job_metadata)
    
    # Display results
    logger.info("\n=== RANKED CANDIDATES ===")
    for candidate in ranked_candidates[:10]:
        logger.info(f"\nRank #{candidate['rank']}: {candidate['file_path']}")
        logger.info(f"Final Score: {candidate['final_score']:.3f}")
        logger.info(f"  - Reranker Score: {candidate['scores']['reranker_score']:.3f}")
        logger.info(f"  - Skill Overlap: {candidate['scores']['skill_overlap']:.3f}")
        logger.info(f"  - Experience Match: {candidate['scores']['experience_match']:.3f}")
        logger.info(f"  - Title Similarity: {candidate['scores']['title_similarity']:.3f}")
        logger.info(f"Extracted Skills: {', '.join(candidate['extracted_data']['skills'][:5])}")

if __name__ == "__main__":
    main()
