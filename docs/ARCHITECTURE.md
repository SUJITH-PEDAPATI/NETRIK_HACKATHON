# Architecture Summary - Task Distribution

## Overview
The HR Automation Resume Pipeline is distributed across 5 core modules + 2 supporting files, following a clear data flow from extraction → structuring → indexing → matching.

---

## File-by-File Breakdown

### 1️⃣ **pdf_extractor.py** - STAGE 1: Text Extraction
**Purpose:** Convert Resume PDFs/DOCX files to raw text

```
Resume File (.pdf/.docx)
         ↓
  PDFExtractor
    ├─ extract_from_pdf()     → pdfplumber (page-by-page)
    ├─ extract_from_docx()    → python-docx (paragraph-by-paragraph)
    └─ extract_text()         → Unified dispatcher
         ↓
    Raw Text String
```

**Key Classes:** `PDFExtractor`
**Dependencies:** pdfplumber, python-docx
**I/O:** File path → Raw text (500-2000 words)

---

### 2️⃣ **ocr_engine.py** - STAGE 1b: OCR (Optional)
**Purpose:** Extract text from scanned/image-based PDFs

```
Scanned PDF
    ↓
  OCREngine (Optional)
    ├─ extract_from_image()      → Tesseract OCR
    └─ extract_from_pdf_page()   → per-page OCR
    ↓
  Raw OCR Text (fallback if pdfplumber fails)
```

**Key Classes:** `OCREngine`
**Dependencies:** pytesseract, opencv-python, Pillow
**When to use:** If pdfplumber extraction is empty (scanned PDFs)

---

### 3️⃣ **docs_extractor.py** - STAGE 2: Structured Data Extraction
**Purpose:** Extract structured resume fields from raw text

```
Raw Resume Text
    ├────────────────────────────┬────────────────────────────┐
    ↓                            ↓
Path A: LLM Extraction      Path B: NER Extraction
(Phi-3-mini)                (GLiNER)
    │                            │
    └─ Prompt Engineering   └─ Entity Recognition
      └─ JSON Output           └─ Entity Categories:
          {                       ├─ skills
           "skills": [...],       ├─ titles
           "experience": [...],   ├─ companies
           "education": [...],    └─ degrees
           "total_years_exp": 0
          }
    │                            │
    └────────────────────────────┴────────────────────────────┘
                     ↓
         Merged Structured Output
         ├─ skills: [] (from both)
         ├─ experience: [] (from LLM)
         ├─ education: [] (from LLM)
         ├─ total_years_exp: int (from LLM)
         ├─ titles: [] (from NER)
         ├─ companies: [] (from NER)
         └─ degrees: [] (from NER)
```

**Key Classes:** `DocsExtractor`
**Methods:**
- `extract_with_llm()` → Phi-3 JSON parsing
- `extract_with_ner()` → GLiNER entity extraction
- `extract()` → Combined (recommended)

**Dependencies:** transformers, torch, gliner
**Models:**
- LLM: microsoft/Phi-3-mini-4k-instruct (3.8B)
- NER: urchade/gliner_base (~300M)

---

### 4️⃣ **parser.py** - STAGE 3: Orchestration
**Purpose:** Coordinate extraction pipeline for single/batch processing

```
Resume Files (single or batch)
    ↓
  ResumeParser
    ├─ parse_file(path) → Single resume
    │    ├─ Text Extraction (pdf_extractor)
    │    ├─ Structure Extraction (docs_extractor)
    │    └─ Metadata Addition (file_path, raw_text)
    │
    └─ parse_folder(path) → All resumes in folder
         ├─ Iterate .pdf/.docx/.doc files
         ├─ Error handling & logging
         └─ Return list of structured resumes

         ↓
    List[Dict] - Parsed Resumes
    [
      {
        "file_path": "resume_1.pdf",
        "raw_text": "...",
        "skills": [...],
        "experience": [...],
        ...
      },
      ...
    ]
```

**Key Classes:** `ResumeParser`
**Methods:**
- `parse_file()` → Single file
- `parse_folder()` → Batch directory

**Dependencies:** pdf_extractor, ocr_engine, docs_extractor
**I/O:** Files → Parsed structured data

---

### 5️⃣ **pipeline.py** - STAGE 4: Matching & Ranking Engine
**Purpose:** Match resumes against job descriptions with explainable scores

```
Parsed Resumes                Job Description
    │                              │
    ▼                              ▼
STAGE 4a: EMBEDDINGS (BGE-Large)
    ├─ encode_text(resume) ──────→ 1024D vector
    └─ encode_text(jd) ──────────→ 1024D vector
              │                        │
              └────────────────┬───────┘
                               ▼
              STAGE 4b: ANN INDEXING (FAISS)
                   ├─ index_resumes(all_embeddings)
                   └─ Build L2 search index
                               ▼
                   STAGE 4c: TOP-K RETRIEVAL
                   ├─ retrieve_top_k(jd_embedding, k=20)
                   └─ Return 20 most similar resumes
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
    STAGE 4d: RERANKING      SCORING 1     SCORING 2
    (BGE-Reranker)           (Skills)      (Experience)
    ├─ Pairwise            ├─ Overlap    ├─ Years vs
    │  cross-encoder         calculation   required
    └─ Score: 0-1           └─ Score: 0-1  └─ Score: 0-1
                │                │            │
                │            SCORING 3       │
                │            (Titles)        │
                │            ├─ Embedding   │
                │            │  similarity  │
                │            └─ Score: 0-1  │
                │                │            │
                └────────────────┼────────────┘
                                 ▼
          FINAL WEIGHTED COMBINATION:
          score = 0.35×reranker
                + 0.30×skill_overlap
                + 0.20×experience
                + 0.15×title_similarity
                                 ▼
          Ranked Candidates (sorted by score)
          [
            {rank, file_path, final_score, scores{}, extracted_data{}},
            ...
          ]
```

**Key Classes:** `ResumeMatcher`
**Methods:**
- `encode_text()` → BGE embeddings
- `index_resumes()` → FAISS indexing
- `retrieve_top_k()` → ANN search
- `rerank_candidates()` → Cross-encoder scoring
- `calculate_skill_overlap()` → Keyword matching
- `calculate_experience_match()` → Years comparison
- `calculate_title_similarity()` → Embedding similarity
- `match_job_description()` → End-to-end pipeline

**Dependencies:** sentence-transformers, faiss-cpu, scikit-learn, numpy
**Models:**
- Embeddings: BAAI/bge-large-en-v1.5 (335M)
- Reranker: BAAI/bge-reranker-large (355M)

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      COMPLETE PIPELINE                          │
└──────────────────────────────────────────────────────────────────┘

INPUT: Resume Files (PDF/DOCX)
   ↓
┌─ pdf_extractor.py ────────────────── TEXT EXTRACTION
│  └─ Raw Text = pdfplumber.extract_text()
│
├─ ocr_engine.py (optional) ───────── SCANNED PDF HANDLING
│  └─ Fallback for image-based PDFs
│
├─ docs_extractor.py ──────────────── STRUCTURED EXTRACTION
│  ├─ LLM Path: Phi-3 JSON parsing
│  └─ NER Path: GLiNER entity recognition
│
├─ parser.py ──────────────────────── ORCHESTRATION
│  └─ Coordinate extraction for single/batch
│
└─ pipeline.py ────────────────────── MATCHING ENGINE
   ├─ Embeddings: BGE-Large (1024D)
   ├─ Indexing: FAISS L2
   ├─ Retrieval: Top-K (k=20)
   ├─ Reranking: BGE-Reranker-Large
   └─ Final Scoring: Weighted combination

OUTPUT: Ranked candidates with explainable scores
```

---

## Module Responsibilities Matrix

| File | Responsibility | Input | Output | Models |
|------|---|---|---|---|
| **pdf_extractor.py** | Text extraction | File paths | Raw text | pdfplumber, python-docx |
| **ocr_engine.py** | OCR fallback | Image/scanned PDF | Raw text (OCR) | Tesseract |
| **docs_extractor.py** | Structured parsing | Raw text | Dict (skills, exp, edu) | Phi-3, GLiNER |
| **parser.py** | Pipeline orchestration | Files/folders | List[Dict] | All above |
| **pipeline.py** | Matching/ranking | Parsed resumes + JD | Ranked list | BGE-Large, BGE-Reranker |

---

## Key Design Decisions

1. **Separation of Concerns:** Each file has a single, clear responsibility
2. **Fault Tolerance:** Fallbacks (e.g., NER-only if LLM fails, no FAISS = brute force)
3. **Modularity:** Can use individual components independently
4. **Explainability:** Component scores shown separately before final combination
5. **Local Execution:** No external APIs, all models run locally
6. **Lightweight:** Phi-3 (3.8B) runs on 8GB RAM, no GPU required

---

## Data Structure Across Stages

```
Stage 1 (pdf_extractor):
├─ Input:  "resume.pdf"
└─ Output: str = "Jane Smith worked at..."

Stage 2 (docs_extractor):
├─ Input:  str = "Jane Smith worked at..."
└─ Output: Dict = {
             "skills": ["Python", "AWS"],
             "experience": ["Software Engineer 2020-2023"],
             "education": ["BS Computer Science"],
             "total_years_exp": 5,
             "titles": ["Engineer", "Lead"],
             "companies": ["TechCorp"]
           }

Stage 3 (parser):
├─ Input:  "resumes_folder/"
└─ Output: List[Dict] = [Resume Dict 1, Resume Dict 2, ...]

Stage 4 (pipeline):
├─ Input:  List[Dict] resumes + str job_description
└─ Output: List[Dict] = [
             {
               "rank": 1,
               "final_score": 0.87,
               "scores": {
                 "reranker_score": 0.89,
                 "skill_overlap": 0.80,
                 "experience_match": 1.0,
                 "title_similarity": 0.85
               }
             },
             ...
           ]
```

---

## Configuration & Customization

- **config.py** - Centralized settings for all modules
  - Model selection
  - Score weights
  - Extraction settings
  - Logging

- **main.py** - Example usage demonstrating full pipeline

---

## Future Extension Points

- Add **multi-language support** (use Qwen2.5-3B-Instruct with language detection)
- Add **industry-specific fine-tuning** (custom Phi-3 models)
- Add **real-time index updates** (incremental FAISS updates)
- Add **resume-to-resume similarity** (diversity scoring)
- Add **explainability UI** (interactive component breakdown)
