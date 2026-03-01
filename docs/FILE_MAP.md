# HR Automation Agent - Implementation Map

## 🗂️ Complete File Structure

```
HR Automation Agent/
│
├── 📋 DOCUMENTATION
│   ├── README.md                    ← Start here! Full guide
│   ├── ARCHITECTURE.md              ← Detailed architecture breakdown
│   └── IMPLEMENTATION.md             ← This implementation summary
│
├── ⚙️ CONFIGURATION
│   ├── config.py                    ← Centralized settings
│   ├── requirements.txt              ← Dependencies
│   └── main.py                       ← Example usage
│
├── 📦 CORE PIPELINE
│   ├── pipeline.py                  ← Matching engine (embeddings→indexing→reranking)
│   │
│   └── resume_extractor/            ← Extraction modules
│       ├── __init__.py               ← Package exports
│       ├── pdf_extractor.py          ← Stage 1: Text extraction (pdfplumber)
│       ├── ocr_engine.py             ← Stage 1b: OCR (Tesseract)
│       ├── docs_extractor.py         ← Stage 2: Structured extraction (Phi-3 + GLiNER)
│       └── parser.py                 ← Stage 3: Orchestration
```

---

## 🔄 Execution Flow with File Mapping

```
START: Resume Files (.pdf/.docx)
│
├─ Resume Files
│  ├─ resume_1.pdf
│  ├─ resume_2.docx
│  └─ resume_3.pdf
│
├─ [STAGE 1] >>> resume_extractor/pdf_extractor.py
│  ├─ PDFExtractor.extract_from_pdf()     ← pdfplumber
│  ├─ PDFExtractor.extract_from_docx()    ← python-docx
│  └─ Output: Raw Text Strings
│
├─ [OPTIONAL] >>> resume_extractor/ocr_engine.py
│  ├─ OCREngine.extract_from_image()      ← pytesseract (if scanned PDF)
│  └─ Output: OCR Text (fallback)
│
├─ [STAGE 2] >>> resume_extractor/docs_extractor.py
│  ├─ LLM Path:
│  │  └─ DocsExtractor.extract_with_llm()
│  │     └─ Model: microsoft/Phi-3-mini-4k-instruct (3.8B)
│  │        └─ Output: {"skills": [...], "experience": [...], ...}
│  │
│  ├─ NER Path:
│  │  └─ DocsExtractor.extract_with_ner()
│  │     └─ Model: urchade/gliner_base (~300M)
│  │        └─ Output: {"skills": [...], "titles": [...], ...}
│  │
│  └─ Combined:
│     └─ DocsExtractor.extract() [RECOMMENDED]
│        └─ Merged: All fields from LLM + NER
│
├─ [STAGE 3] >>> resume_extractor/parser.py
│  ├─ ResumeParser.parse_file()  (single resume)
│  ├─ ResumeParser.parse_folder() (batch)
│  └─ Output: List[Dict] = Parsed Resumes with metadata
│
├─ [STAGE 4] >>> pipeline.py
│  │
│  ├─ 4a: Embeddings
│  │  ├─ ResumeMatcher.encode_text()
│  │  ├─ Model: BAAI/bge-large-en-v1.5 (335M)
│  │  └─ Output: 1024-dimensional vectors
│  │
│  ├─ 4b: ANN Indexing
│  │  ├─ ResumeMatcher.index_resumes()
│  │  ├─ Library: FAISS (or fallback: sklearn brute force)
│  │  └─ Output: Searchable index
│  │
│  ├─ 4c: Top-K Retrieval
│  │  ├─ ResumeMatcher.retrieve_top_k(job_description, k=20)
│  │  └─ Output: Top 20 similar resumes
│  │
│  ├─ 4d: Reranking
│  │  ├─ ResumeMatcher.rerank_candidates()
│  │  ├─ Model: BAAI/bge-reranker-large (355M)
│  │  └─ Output: Reranked list with scores
│  │
│  └─ 4e: Final Scoring
│     ├─ ResumeMatcher.calculate_skill_overlap()     → 0-1 score
│     ├─ ResumeMatcher.calculate_experience_match()  → 0-1 score
│     ├─ ResumeMatcher.calculate_title_similarity()  → 0-1 score
│     └─ Weighted Combination:
│        └─ final_score = 0.35×reranker + 0.30×skills + 0.20×exp + 0.15×title
│
├─ [CONFIGURATION] >>> config.py
│  ├─ Model selection
│  ├─ Scoring weights
│  ├─ Extraction settings
│  └─ Computation preferences
│
├─ [EXAMPLE] >>> main.py
│  └─ Full pipeline demonstration with logging
│
END: Ranked Candidates List
├─ Rank 1: resume_1.pdf (score: 0.87)
│  ├─ reranker_score: 0.89
│  ├─ skill_overlap: 0.80
│  ├─ experience_match: 1.0
│  └─ title_similarity: 0.85
│
├─ Rank 2: resume_2.docx (score: 0.82)
│  └─ ...
│
└─ Rank 3: resume_3.pdf (score: 0.78)
   └─ ...
```

---

## 📊 Module Dependency Graph

```
User Code (main.py)
    │
    ├─→ ResumeParser (parser.py)
    │    ├─→ PDFExtractor (pdf_extractor.py)
    │    ├─→ OCREngine (ocr_engine.py) [optional]
    │    └─→ DocsExtractor (docs_extractor.py)
    │         ├─→ transformers (Phi-3-mini LLM)
    │         └─→ gliner (GLiNER NER)
    │
    └─→ ResumeMatcher (pipeline.py)
         ├─→ SentenceTransformer (BGE-Large embeddings)
         ├─→ CrossEncoder (BGE-Reranker reranking)
         └─→ faiss (FAISS ANN indexing) [optional: fallback available]
```

---

## 🎯 Key Class Locations

### Text Extraction
```python
from resume_extractor import PDFExtractor, OCREngine

pdf = PDFExtractor()
text = pdf.extract_text("resume.pdf")  # Your file here
```
**Files:** pdf_extractor.py, ocr_engine.py

---

### Structured Extraction
```python
from resume_extractor import DocsExtractor

extractor = DocsExtractor()
structured = extractor.extract(raw_text)  # {skills, experience, education, ...}
```
**File:** docs_extractor.py
**Models:** Phi-3-mini (LLM), GLiNER (NER)

---

### Batch Processing
```python
from resume_extractor import ResumeParser

parser = ResumeParser()
all_resumes = parser.parse_folder("./resumes")  # Parsed: List[Dict]
```
**File:** parser.py

---

### Matching & Ranking
```python
from pipeline import ResumeMatcher

matcher = ResumeMatcher()
matcher.index_resumes(all_resumes)

results = matcher.match_job_description(
    job_description="Senior Python engineer with AWS...",
    job_metadata={"skills": ["Python", "AWS"], "years_experience": 5}
)
# Results: Ranked candidates with explainable scores
```
**File:** pipeline.py
**Models:** BGE-Large (embeddings), BGE-Reranker (reranking), FAISS (indexing)

---

## 🔧 Configuration Hierarchy

```
config.py (centralized settings)
    │
    ├─→ LLM_MODEL (used by docs_extractor.py)
    ├─→ NER_MODEL (used by docs_extractor.py)
    ├─→ EMBEDDING_MODEL (used by pipeline.py)
    ├─→ RERANKER_MODEL (used by pipeline.py)
    ├─→ SCORE_WEIGHTS (used by pipeline.py)
    ├─→ USE_OCR (used by parser.py)
    ├─→ TESSERACT_PATH (used by ocr_engine.py)
    └─→ USE_FAISS (used by pipeline.py)
```

**To customize:** Edit config.py, all modules respect these settings

---

## 💾 Data Structure Evolution

```
Stage 1 (pdf_extractor.py):
├─ Input:  str (file path)
└─ Output: str (raw resume text ~500-2000 words)

Stage 2 (docs_extractor.py):
├─ Input:  str (raw text)
└─ Output: Dict {
    "skills": ["Python", "AWS", ...],
    "experience": ["Software Engineer 2020-2023", ...],
    "education": ["BS Computer Science", ...],
    "total_years_exp": 5,
    "titles": ["Engineer", "Lead", ...],
    "companies": ["TechCorp", ...],
    "degrees": ["BS", ...]
}

Stage 3 (parser.py):
├─ Input:  str (folder path)
└─ Output: List[Dict] [
    {
      "file_path": "resume_1.pdf",
      "raw_text": "...",
      "skills": [...],
      "experience": [...],
      ...
    },
    ...
]

Stage 4 (pipeline.py):
├─ Input:  List[Dict] + str (job description)
└─ Output: List[Dict] [
    {
      "rank": 1,
      "file_path": "resume_1.pdf",
      "final_score": 0.87,
      "scores": {
        "reranker_score": 0.89,
        "skill_overlap": 0.80,
        "experience_match": 1.0,
        "title_similarity": 0.85
      },
      "extracted_data": {
        "skills": [...],
        "experience": [...],
        ...
      }
    },
    ...
]
```

---

## 📦 Dependencies by Module

| Module | Direct Dependencies |
|--------|-------------------|
| pdf_extractor.py | pdfplumber, python-docx, pathlib |
| ocr_engine.py | pytesseract, opencv-python, Pillow |
| docs_extractor.py | transformers, torch, gliner |
| parser.py | pathlib, logging, typing |
| pipeline.py | sentence-transformers, numpy, scikit-learn, faiss-cpu |
| config.py | - (pure Python config) |
| main.py | parser, pipeline |

**Install all:** `pip install -r requirements.txt`

---

## ✅ Implementation Checklist

- [x] **Stage 1:** PDF/DOCX text extraction (pdf_extractor.py)
- [x] **Stage 1b:** OCR for scanned PDFs (ocr_engine.py)
- [x] **Stage 2:** LLM-based structured extraction (docs_extractor.py)
- [x] **Stage 2:** NER-based entity extraction (docs_extractor.py)
- [x] **Stage 3:** Batch orchestration (parser.py)
- [x] **Stage 4a:** Semantic embeddings (pipeline.py)
- [x] **Stage 4b:** FAISS ANN indexing (pipeline.py)
- [x] **Stage 4c:** Top-K retrieval (pipeline.py)
- [x] **Stage 4d:** Cross-encoder reranking (pipeline.py)
- [x] **Stage 4e:** Weighted scoring (pipeline.py)
- [x] **Config:** Centralized settings (config.py)
- [x] **Example:** Full demo (main.py)
- [x] **Docs:** Complete documentation (README.md, ARCHITECTURE.md)

---

## 🚀 Getting Started

1. **Install:** `pip install -r requirements.txt`
2. **Configure:** Edit config.py if needed
3. **Run Example:** `python main.py` (update path first)
4. **Integrate:** Import classes as shown above

---

## 📞 Support

For issues or customization:
- Check config.py for quick tweaks
- Read ARCHITECTURE.md for detailed design
- Inspect logging output for debugging
- Review main.py for usage patterns

**Status: ✅ Ready to use!**
