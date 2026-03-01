import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class ResumeMatcher:
    """Matching pipeline: embeddings → ANN indexing → reranking → scoring"""

    def __init__(self):
        """Initialize embeddings and reranker models"""
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("BAAI/bge-large-en-v1.5")
            logger.info("Loaded BGE-Large embedding model")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.encoder = None

        try:
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder("BAAI/bge-reranker-large")
            logger.info("Loaded BGE-Reranker-Large model")
        except Exception as e:
            logger.warning(f"Reranker not available: {e}")
            self.reranker = None

        try:
            import faiss
            self.faiss = faiss
            logger.info("FAISS available for ANN indexing")
        except Exception as e:
            logger.warning(f"FAISS not available: {e}")
            self.faiss = None

        self.resume_embeddings = []
        self.resume_data = []
        self.index = None

    def encode_text(self, text: str) -> np.ndarray:
        """Encode text to embeddings using BGE-Large"""
        if not self.encoder:
            return np.zeros(1024)
        return self.encoder.encode(text, convert_to_numpy=True)

    def index_resumes(self, resumes: List[Dict]) -> None:
        """Build ANN index (FAISS) for all resume embeddings"""
        if not self.encoder:
            logger.error("Encoder not initialized")
            return

        self.resume_data = resumes
        embeddings = []

        for resume in resumes:
            # Create section embeddings for weighted field matching
            resume_text = resume.get("raw_text", "")
            embedding = self.encode_text(resume_text)
            embeddings.append(embedding)

        embeddings = np.array(embeddings).astype(np.float32)
        self.resume_embeddings = embeddings

        # Build FAISS index if available
        if self.faiss:
            try:
                dimension = embeddings.shape[1]
                self.index = self.faiss.IndexFlatL2(dimension)
                self.index.add(embeddings)
                logger.info(f"Indexed {len(resumes)} resumes")
            except Exception as e:
                logger.error(f"Error building FAISS index: {e}")
        else:
            logger.warning("FAISS not available, using simple similarity search")

    def retrieve_top_k(self, job_description: str, k: int = 10) -> List[Tuple[int, float]]:
        """Retrieve top-K similar resumes using ANN"""
        jd_embedding = self.encode_text(job_description).reshape(1, -1).astype(np.float32)

        if self.faiss and self.index:
            try:
                distances, indices = self.index.search(jd_embedding, min(k, len(self.resume_data)))
                return [(int(idx), float(1 / (1 + dist))) for idx, dist in zip(indices[0], distances[0])]
            except Exception as e:
                logger.error(f"Error in FAISS search: {e}")
        
        # Fallback: simple cosine similarity
        if len(self.resume_embeddings) == 0:
            return []
        
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(jd_embedding, self.resume_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:k]
        return [(int(idx), float(similarities[idx])) for idx in top_indices]

    def rerank_candidates(self, job_description: str, candidate_indices: List[int]) -> List[Dict]:
        """Rerank candidates using cross-encoder (pairwise scoring)"""
        if not self.reranker or len(candidate_indices) == 0:
            return [{"index": idx, "reranker_score": 0.5} for idx in candidate_indices]

        try:
            pairs = [(job_description, self.resume_data[idx].get("raw_text", "")) 
                     for idx in candidate_indices]
            scores = self.reranker.predict(pairs)
            
            results = []
            for idx, score in zip(candidate_indices, scores):
                results.append({"index": idx, "reranker_score": float(score)})
            
            return sorted(results, key=lambda x: x["reranker_score"], reverse=True)
        except Exception as e:
            logger.error(f"Error in reranking: {e}")
            return [{"index": idx, "reranker_score": 0.5} for idx in candidate_indices]

    def calculate_skill_overlap(self, jd_skills: List[str], resume_data: Dict) -> float:
        """Calculate skill overlap score"""
        if not jd_skills:
            return 0.0
        
        resume_skills = set(skill.lower() for skill in resume_data.get("skills", []))
        jd_skills_lower = set(skill.lower() for skill in jd_skills)
        
        if len(jd_skills_lower) == 0:
            return 0.0
        
        overlap = len(resume_skills.intersection(jd_skills_lower))
        return overlap / len(jd_skills_lower)

    def calculate_experience_match(self, required_years: int, resume_data: Dict) -> float:
        """Calculate experience match score"""
        resume_years = resume_data.get("total_years_exp", 0)
        if required_years == 0:
            return 1.0
        return min(1.0, resume_years / required_years)

    def calculate_title_similarity(self, required_title: str, resume_data: Dict) -> float:
        """Calculate job title similarity"""
        if not self.encoder or not required_title:
            return 0.5
        
        resume_titles = resume_data.get("titles", [])
        if not resume_titles:
            return 0.0
        
        required_embedding = self.encode_text(required_title)
        title_similarities = [
            float(np.dot(required_embedding, self.encode_text(title)) / 
                  (np.linalg.norm(required_embedding) * np.linalg.norm(self.encode_text(title)) + 1e-10))
            for title in resume_titles
        ]
        return max(title_similarities) if title_similarities else 0.0

    def match_job_description(self, job_description: str, job_metadata: Optional[Dict] = None) -> List[Dict]:
        """Full matching pipeline: ANN retrieval → reranking → final scoring"""
        if not self.resume_data:
            logger.warning("No resumes indexed")
            return []

        job_metadata = job_metadata or {}
        required_skills = job_metadata.get("skills", [])
        required_years = job_metadata.get("years_experience", 0)
        required_title = job_metadata.get("job_title", "")

        # Step 1: Retrieve top candidates using ANN
        retrieved = self.retrieve_top_k(job_description, k=20)
        retrieved_indices = [idx for idx, _ in retrieved]

        # Step 2: Rerank with cross-encoder
        reranked = self.rerank_candidates(job_description, retrieved_indices)
        reranked_indices = [r["index"] for r in reranked]
        reranker_scores = {r["index"]: r["reranker_score"] for r in reranked}

        # Step 3: Calculate final scores with weighted combination
        results = []
        for idx in reranked_indices:
            resume = self.resume_data[idx]
            
            skill_overlap = self.calculate_skill_overlap(required_skills, resume)
            experience_match = self.calculate_experience_match(required_years, resume)
            title_similarity = self.calculate_title_similarity(required_title, resume)
            reranker_score = reranker_scores.get(idx, 0.5)
            
            # Weighted final score
            final_score = (
                0.35 * reranker_score +
                0.30 * skill_overlap +
                0.20 * experience_match +
                0.15 * title_similarity
            )
            
            results.append({
                "rank": len(results) + 1,
                "file_path": resume.get("file_path", ""),
                "final_score": float(final_score),
                "scores": {
                    "reranker_score": float(reranker_score),
                    "skill_overlap": float(skill_overlap),
                    "experience_match": float(experience_match),
                    "title_similarity": float(title_similarity)
                },
                "extracted_data": {
                    "skills": resume.get("skills", []),
                    "experience": resume.get("experience", []),
                    "education": resume.get("education", []),
                    "total_years_exp": resume.get("total_years_exp", 0)
                }
            })
        
        return results
