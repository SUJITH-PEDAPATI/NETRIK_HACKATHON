"""
Configuration for HR Automation Resume Pipeline
Edit this file to customize models, weights, and behavior
"""

# ============================================================================
# MODEL SELECTION
# ============================================================================

# LLM for structured resume extraction
LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"  # 3.8B, instruction-following
# Alternatives:
# - "google/gemma-2-2b-it"  # 2B, very fast
# - "mistralai/Mistral-7B-Instruct-v0.3"  # 7B, best quality (needs GPU/16GB)
# - "Qwen/Qwen2.5-3B-Instruct"  # 3B, multilingual

# NER model for entity extraction
NER_MODEL = "urchade/gliner_base"

# Embedding model for semantic similarity
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"  # 335M, 1024-dimensional
# Alternatives:
# - "BAAI/bge-base-en-v1.5"  # Smaller (109M)
# - "all-MiniLM-L6-v2"  # Ultra-light (22M)

# Reranking model (cross-encoder)
RERANKER_MODEL = "BAAI/bge-reranker-large"

# ============================================================================
# COMPUTATION
# ============================================================================

# Use GPU if available
USE_GPU = True

# Device selection (auto-detect by default)
DEVICE = None  # None = auto-detect, or set to 0, 1, etc. for specific GPU

# Data type for inference
# "float16" = faster but less precise (GPU recommended)
# "float32" = more precise (CPU or GPU)
DTYPE = "float16"

# ============================================================================
# TEXT EXTRACTION
# ============================================================================

# Enable OCR for scanned PDFs (slower but captures image text)
USE_OCR = False

# Path to Tesseract executable (if not in PATH)
# Windows example: r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_PATH = None

# ============================================================================
# EXTRACTION SETTINGS
# ============================================================================

# Use LLM for structured extraction
USE_LLM_EXTRACTION = True

# Use NER for entity-level extraction
USE_NER_EXTRACTION = True

# Max tokens for LLM generation
LLM_MAX_TOKENS = 1024

# Temperature for LLM (0 = deterministic, 1 = random)
LLM_TEMPERATURE = 0.3

# ============================================================================
# MATCHING & RANKING
# ============================================================================

# Final score weights (must sum to 1.0)
SCORE_WEIGHTS = {
    "reranker_score": 0.35,      # Cross-encoder semantic match
    "skill_overlap": 0.30,        # Exact keyword matching
    "experience_match": 0.20,     # Years of experience
    "title_similarity": 0.15      # Job title embedding similarity
}

# Verify weights sum to 1.0
assert abs(sum(SCORE_WEIGHTS.values()) - 1.0) < 0.01, "Weights must sum to 1.0!"

# Number of candidates to retrieve before reranking
TOP_K_RETRIEVAL = 20

# Number of final candidates to return
TOP_K_FINAL = 10

# ============================================================================
# ANN INDEX SETTINGS
# ============================================================================

# Use FAISS for fast approximate nearest neighbor search
USE_FAISS = True

# FAISS index type
# "L2" = Euclidean distance (default)
# "IP" = Inner product (dot product)
FAISS_INDEX_TYPE = "L2"

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# BATCH PROCESSING
# ============================================================================

# Batch size for embedding generation
EMBEDDING_BATCH_SIZE = 32

# Number of workers for parallel file reading
NUM_WORKERS = 4

# ============================================================================
# CACHING
# ============================================================================

# Cache embeddings to disk (faster subsequent loads)
CACHE_EMBEDDINGS = True

CACHE_DIR = ".cache"

# ============================================================================
# OUTPUT
# ============================================================================

# Include raw text in results (verbose)
INCLUDE_RAW_TEXT = False

# Precision for floating point scores
SCORE_PRECISION = 3
