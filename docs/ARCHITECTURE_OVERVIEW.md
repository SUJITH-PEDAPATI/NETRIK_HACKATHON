# 🏗️ HR Automation Agent - Complete Architecture Overview

## 📊 Project Structure & Architectural Patterns

```
HR Automation Agent/
├── Phase 1: Resume Screening (interview_engine/)
├── Phase 3: Interview Scheduling (phase3_scheduling/)
├── Phase 4: Leave Management (phase4_leave/)
├── Phase 6: Escalation Detection (phase6_escalation/)
├── Presentation Layer (ui/)
├── Cross-Cutting Concerns (utils/)
├── Resume Extraction (resume extractor/)
└── Orchestration (pipeline.py, main.py)
```

---

## 📁 FOLDER-BY-FOLDER BREAKDOWN

### 1. 🧠 **interview_engine/** - Candidate Screening & Evaluation
**Role:** Phase 1 - The first stage of recruitment pipeline  
**Architecture Pattern:** Plugin-based Evaluator Pattern

#### Structure:
```
interview_engine/
├── question_bank/
│   ├── adaptive_engine.py       # AI-driven question selection
│   ├── ai_features.py           # LLM-powered analysis
│   ├── analytics.py             # Evaluation metrics
│   ├── assessor.py              # Skill assessment logic
│   ├── behavioral.py            # Behavioral question bank
│   ├── culture.py               # Cultural fit evaluation
│   ├── evaluator.py             # Core evaluator orchestrator
│   ├── models.py                # Data models
│   ├── registry.py              # Question/skill registry
│   ├── situational.py           # Situational questions
│   ├── skill_aliases.py         # Skill mapping/normalization
│   ├── technical.py             # Technical skill questions
│   └── __init__.py
└── IMPLEMENTATION_SUMMARY.md
```

#### Architecture:
```
┌─────────────────────────────────────┐
│      EVALUATOR (Orchestrator)       │ Main controller
├─────────────────────────────────────┤
│ ┌─────────┬────────┬────────────┐   │
│ │Technical│Cultural│Behavioral  │   │ Question generators
│ │Questions│Fit     │Questions   │   │
│ └─────────┴────────┴────────────┘   │
│ ┌─────────────────────────────────┐ │
│ │  Adaptive Engine (AI)           │ │ Smart question selection
│ │  - Selects next Q based on      │ │
│ │    previous answers             │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │  Assessor Module                │ │ Scoring & analysis
│ │  - Scores responses             │ │
│ │  - Matches skills               │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

#### Design Patterns Used:
- **Plugin/Extensible Pattern** - Question banks pluggable
- **Strategy Pattern** - Different assessment strategies
- **Registry Pattern** - Skill/question lookup
- **Adapter Pattern** - LLM integration (ai_features)

#### Key Outcomes:
- Candidate ranking score (0-100)
- Skills matched vs. required
- Behavioral assessment
- Cultural fit score

---

### 2. 📅 **phase3_scheduling/** - Interview Calendar Management
**Role:** Phase 3 - Schedule interviews optimally  
**Architecture Pattern:** Constraint Satisfaction Problem (CSP) Solver

#### Structure:
```
phase3_scheduling/
├── core/
│   ├── scheduler.py              # Main scheduler (state mgmt)
│   ├── csp_solver.py             # Constraint solver (optimal)
│   ├── greedy_solver.py          # Fast approximation
│   ├── conflict_analysis.py      # Conflict detection
│   └── __init__.py
├── models/
│   ├── schema.py                 # Data structures
│   ├── types.py                  # Type definitions
│   └── __init__.py
├── loaders/
│   ├── availability_loader.py    # Load availability
│   ├── csv_loader.py             # CSV import
│   ├── json_loader.py            # JSON import
│   ├── pipeline_bridge.py        # Integration
│   └── __init__.py
├── reporting/
│   ├── ical_exporter.py          # iCalendar export
│   ├── schedule_reporter.py      # Reports
│   └── __init__.py
├── scheduling_pipeline.py        # Main pipeline
└── ADVANCED_FEATURES.md
```

#### Architecture:
```
┌──────────────────────────────────────┐
│    Scheduling Pipeline               │ Orchestrator
├──────────────────────────────────────┤
│ ┌────────────────────────────────┐   │
│ │  Input Loaders                 │   │ Load data
│ │  - CSV, JSON, API              │   │
│ └────────────────────────────────┘   │
│         ↓                             │
│ ┌────────────────────────────────┐   │
│ │  Availability Analysis         │   │ Parse constraints
│ │  - Time slots                  │   │
│ │  - Resources                   │   │
│ │  - Conflicts                   │   │
│ └────────────────────────────────┘   │
│         ↓                             │
│ ┌────────────────────────────────┐   │ Solvers can
│ │  ┌──────────────┐┌──────────┐ │   │ be swapped
│ │  │ CSP Solver   ││Greedy    │ │   │
│ │  │(Optimal)     ││(Fast)    │ │   │
│ │  └──────────────┘└──────────┘ │   │
│ └────────────────────────────────┘   │
│         ↓                             │
│ ┌────────────────────────────────┐   │
│ │  Conflict Resolution           │   │ Handle overlaps
│ │  - Detect & notify             │   │
│ └────────────────────────────────┘   │
│         ↓                             │
│ ┌────────────────────────────────┐   │
│ │  Reporting & Export            │   │ Output formats
│ │  - iCalendar                   │   │
│ │  - PDF, JSON                   │   │
│ └────────────────────────────────┘   │
└──────────────────────────────────────┘
```

#### Design Patterns Used:
- **Strategy Pattern** - CSP vs Greedy solver swappable
- **Constraint Satisfaction** - Mathematical optimization
- **Factory Pattern** - Loader selection
- **Template Method** - Pipeline stages

#### Key Algorithms:
- **CSP Solver**: Backtracking with constraint propagation
- **Greedy Solver**: Fast approximation for large datasets
- **Conflict Analysis**: Graph-based conflict detection

#### Key Outcomes:
- Optimal calendar (minimal conflicts)
- Resource utilization metrics
- Exportable calendar (iCalendar format)
- Conflict reports

---

### 3. 🏖️ **phase4_leave/** - Leave Request Management
**Role:** Phase 4 - Policy-based leave approval  
**Architecture Pattern:** State Machine + Policy Engine

#### Structure:
```
phase4_leave/
├── engine/
│   ├── leave_policy_engine.py   # Core deterministic logic
│   ├── rule_definitions.py      # Policy rules
│   ├── overlap_checker.py        # Conflict detection
│   ├── validators.py            # Request validation
│   └── __init__.py
├── models/
│   ├── leave_type_enum.py       # Leave types
│   ├── leave_policy_model.py    # Policy definitions
│   ├── leave_request_model.py   # Request data
│   ├── leave_balance_model.py   # Balance tracking
│   ├── approval_workflow_model.py # Workflow
│   ├── leave_schema.py          # Schemas
│   └── __init__.py
├── persistence/
│   ├── leave_repository.py      # Data access
│   └── __init__.py
├── reporting/
│   ├── leave_reporter.py        # Reports
│   └── __init__.py
├── state_management/
│   ├── core/
│   │   ├── fsm_definition.py    # State machine definition
│   │   ├── guards.py            # Transition guards
│   │   ├── transitions.py       # State transitions
│   │   └── __init__.py
│   ├── persistence/
│   │   ├── json_store.py        # JSON storage
│   │   ├── memory_store.py      # In-memory storage
│   │   ├── sqlite_store.py      # SQLite storage
│   │   ├── repository.py        # Data access
│   │   └── __init__.py
│   ├── service/
│   │   ├── state_service.py     # State service
│   │   ├── event_hooks.py       # Event handlers
│   │   ├── audit_logger.py      # Audit trail
│   │   └── __init__.py
│   ├── cli/
│   │   ├── state_cli.py         # CLI commands
│   │   └── __init__.py
│   └── __init__.py
└── README.md
```

#### Architecture:
```
┌─────────────────────────────────────────────────┐
│         LEAVE POLICY ENGINE (Deterministic)     │ Core logic
├─────────────────────────────────────────────────┤
│  1. Policy Check:                               │
│     - Is leave type allowed?                    │
│     - Max days per year exceeded?               │
│     - Required documents present?               │
│                                                 │
│  2. Balance Check:                             │
│     - Does employee have balance?               │
│     - Account for pending requests?             │
│     - Include carryforward?                     │
│                                                 │
│  3. Overlap Check:                             │
│     - Any conflicts with other leaves?          │
│     - Team coverage requirements?               │
│     - Department limits?                        │
│                                                 │
│  4. Approval Check:                            │
│     - Manager approval needed?                  │
│     - Is it auto-approvable?                    │
│                                                 │
│  DECISION: → Approved / Rejected / Pending      │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│     STATE MACHINE (Workflow Coordination)        │ Orchestration
├─────────────────────────────────────────────────┤
│  Draft → Submitted → Pending → Approved/Rejected│
│  ↓       ↓           ↓         ↓                │
│  [Guards active throughout]                     │
│  [Transitions trigger hooks]                    │
│  [All events audited]                           │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│    PERSISTENCE LAYER (Pluggable Storage)        │ Data layer
├─────────────────────────────────────────────────┤
│  ┌─────────────┬──────────────┬──────────────┐  │
│  │ JSON Store  │ Memory Store │ SQLite Store │  │
│  │(Dev/Demo)   │(Fast)        │(Production)  │  │
│  └─────────────┴──────────────┴──────────────┘  │
└─────────────────────────────────────────────────┘
```

#### Design Patterns Used:
- **Finite State Machine (FSM)** - Workflow management
- **Policy Pattern** - Business rules
- **Strategy Pattern** - Pluggable storage backends
- **Guard Clause Pattern** - Transition validation
- **Event-Driven** - Hook-based notifications

#### Key Features:
- **Tenure-based Entitlements** - Different rules per seniority
- **Accrual System** - Monthly accumulation
- **Carryforward Logic** - Year-end handling
- **Team Coverage** - Department constraints
- **Auto-approval** - For simple requests

#### Key Outcomes:
- Leave decision (Approved/Rejected)
- Decision reasoning & policy justification
- Balance updates
- Audit trail of all changes

---

### 4. 🚨 **phase6_escalation/** - Case Escalation & Monitoring
**Role:** Phase 6 - Detect and manage escalated cases  
**Architecture Pattern:** Hybrid Detection (Rule + ML) with Orchestration

#### Structure:
```
phase6_escalation/
├── engine/
│   ├── escalation_service.py    # Main orchestrator
│   ├── rule_engine.py           # Keyword matching
│   ├── classifier_engine.py     # ML/LLM classifier
│   ├── decision_combiner.py     # Hybrid decision logic
│   └── batch_processor.py       # Batch operations
├── models/
│   ├── escalation_types.py      # Enums & categories
│   ├── escalation_schema.py     # Data models
│   ├── escalation_config.py     # Configuration
│   └── __init__.py
├── persistence/
│   ├── escalation_repository.py # Data access & audit
│   └── __init__.py
├── utils/
│   ├── text_preprocessor.py     # Text normalization
│   ├── keyword_matcher.py       # Pattern matching
│   └── __init__.py
├── api/
│   ├── escalation_api.py        # REST endpoints
│   └── __init__.py
├── audit/
│   ├── audit_log.py             # Audit logging
│   ├── audit_cli_helpers.py     # CLI utilities
│   └── __init__.py
├── cli/
│   ├── escalation_cli.py        # Command-line tool
│   └── __init__.py
├── demo/
│   ├── demo_runner.py           # Demo scenarios
│   └── __init__.py
└── __init__.py
```

#### Architecture:
```
┌────────────────────────────────────────────┐
│   INPUT: Escalation Request                │ Content to analyze
└────────────────┬───────────────────────────┘
                 ↓
┌────────────────────────────────────────────┐
│   TEXT PREPROCESSING                       │ Normalize input
│   - Expand contractions                    │
│   - Remove special chars                   │
│   - Tokenization                           │
│   - Entity extraction                      │
└────────────────┬───────────────────────────┘
                 ↓
         ┌───────┴────────┐
         ↓                ↓
    ┌─────────────┐  ┌──────────────┐
    │ RULE ENGINE │  │ ML CLASSIFIER│ Parallel detection
    │             │  │              │
    │ Keyword     │  │ LLM/ML Model │
    │ matching    │  │ Classification
    │ w/ scoring  │  │ w/ confidence
    └─────┬───────┘  └──────┬───────┘
          │                 │
          └────────┬────────┘
                   ↓
        ┌──────────────────────┐
        │ DECISION COMBINER    │ Hybrid logic
        │                      │
        │ Strategy:            │
        │ - Rule Primary       │
        │ - ML Primary         │
        │ - Consensus          │
        │ - Weighted Vote      │
        │ - Ensemble           │
        └────────┬─────────────┘
                 ↓
        ┌──────────────────────┐
        │ ESCALATION SERVICE   │ Orchestration
        │                      │
        │ If escalated:        │
        │  - Create case       │
        │  - Assign handler    │
        │  - Notify team       │
        │  - Set SLA           │
        │  - Log audit         │
        └────────┬─────────────┘
                 ↓
        ┌──────────────────────┐
        │ OUTPUT: Case Record  │ Persistence
        │ + Audit Trail        │
        └──────────────────────┘
```

#### Design Patterns Used:
- **Orchestrator Pattern** - EscalationService coordinates
- **Strategy Pattern** - Rule, ML, Combiner swappable
- **Adapter Pattern** - API, CLI, Demo adapters
- **Repository Pattern** - Data persistence
- **Repository + Audit Pattern** - Event tracking
- **Factory Pattern** - Case/notification creation

#### Key Detection Methods:
- **Rule Engine**: 11 categories, keyword matching, confidence scoring
- **ML Classifier**: LLM integration, probability distribution
- **Decision Combiner**: Multiple combination strategies
- **Batch Processing**: Process 100+ items concurrently

#### Key Outcomes:
- Escalation case created (if needed)
- Severity level assigned
- Category classified
- Assignment to handling team
- SLA deadline set
- Audit trail recorded

---

### 5. 📄 **resume extractor/** - Document Processing
**Role:** Pre-processing - Extract text from resumes  
**Architecture Pattern:** Pipeline Pattern

#### Structure:
```
resume extractor/
├── ocr_engine.py                # Optical character recognition
├── pdf_extractor.py             # PDF text extraction
├── parser.py                    # Resume parsing
├── docs_extractor.py            # DOCX handling
└── __init__.py
```

#### Architecture:
```
Raw Resume File
    ↓
┌─────────────────────┐
│ Format Detector     │
└──────┬──────────────┘
       ├─→ PDF? → PDF Extractor
       ├─→ DOCX? → DOCX Extractor
       └─→ Image/Scanned? → OCR Engine
           ↓
┌──────────────────────┐
│ Text Parser          │ Parse sections
│ - Extract fields     │
│ - Normalize text     │
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Structured Output    │
│ [ skills, exp, edu ] │
└──────────────────────┘
```

---

### 6. 🖥️ **ui/** - Streamlit Dashboard (Presentation Layer)
**Role:** Web interface for all phases  
**Architecture Pattern:** MVC + Separation of Concerns

#### Structure:
```
ui/
├── app.py                       # Main Streamlit app (600+ lines)
├── components/
│   ├── streamlit_components.py  # Reusable UI widgets
│   └── __init__.py
└── __init__.py

UI Tabs:
1. 📄 Resume Upload     → Ranking display
2. 🗓 Scheduling        → Calendar view
3. 🏖 Leave Management  → Policy visualization
4. 📊 Candidate History → State timeline
5. 🚨 Escalation        → Case monitoring
6. ⚙️ Export & Metrics   → System health
```

#### Architecture:
```
┌──────────────────────────────────────────┐
│     STREAMLIT APP (Frontend)             │
├──────────────────────────────────────────┤
│                                          │
│  Sidebar (Configuration)                 │
│  ├─ System Status                        │
│  ├─ Settings Toggle                      │
│  └─ Quick Actions                        │
│                                          │
│  Main Content (6 Tabs)                   │
│  ├─ Resume Upload                        │
│  ├─ Scheduling                           │
│  ├─ Leave Management                     │
│  ├─ Candidate History                    │
│  ├─ Escalation Monitor                   │
│  └─ Settings & Export                    │
│                                          │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│    BUSINESS LOGIC LAYER                  │
│ (Imported from utils & phase modules)    │
└──────┬───────────────────────────────────┘
       ↓
┌──────────────────────────────────────────┐
│    DATA ACCESS LAYER                     │
│ (Repositories, Storage)                  │
└──────────────────────────────────────────┘
```

#### Design Patterns Used:
- **MVC Pattern** - Separation of model, view, control
- **Component Pattern** - Reusable UI widgets
- **State Management** - Streamlit session state

#### Key Features:
- Real-time metrics (plotly charts)
- Sample data for demo
- Export button (calls export_manager)
- Decision reasoning display
- Audit log viewer

---

### 7. ⚙️ **utils/** - Cross-Cutting Concerns
**Role:** Shared utilities used by all phases  
**Architecture Pattern:** Utility Library + Dependency Injection

#### Structure:
```
utils/
├── export_manager.py            # 📤 Standardized JSON export
├── logging_system.py            # 📋 Audit logging system
├── explanation_engine.py        # 💡 Decision reasoning
├── metrics_dashboard.py         # 📊 KPI tracking
└── __init__.py
```

#### Architecture:
```
┌──────────────────────────────────────────┐
│    EXPORT MANAGER                        │
├──────────────────────────────────────────┤
│ export_results():                        │
│  ├─ Rankings                             │
│  ├─ Interviews                           │
│  ├─ Schedule                             │
│  ├─ Leave Decisions                      │
│  ├─ State Logs                           │
│  └─ Escalations                          │
│                                          │
│ Features:                                │
│  ├─ JSON/CSV/PDF export                 │
│  ├─ Hash verification                   │
│  └─ Structure validation                 │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│    LOGGING SYSTEM                        │
├──────────────────────────────────────────┤
│ Structured Logging:                      │
│  ├─ Event logging (JSON format)          │
│  ├─ 19 audit action types                │
│  ├─ User tracking                        │
│  └─ Audit trail generation               │
│                                          │
│ Features:                                │
│  ├─ Console + file output                │
│  ├─ Event buffering                      │
│  └─ Compliance logging                   │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│    EXPLANATION ENGINE                    │
├──────────────────────────────────────────┤
│ Generate Human-Readable Explanations:    │
│  ├─ Resume score breakdown               │
│  ├─ Leave decision reasoning             │
│  ├─ Scheduling conflict resolution       │
│  └─ Escalation triggers                  │
│                                          │
│ Purpose:                                 │
│  └─ Interpretability for judges          │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│    METRICS DASHBOARD                     │
├──────────────────────────────────────────┤
│ Real-Time System Metrics:                │
│  ├─ Performance KPIs                     │
│  ├─ Quality metrics                      │
│  ├─ Pipeline efficiency                  │
│  ├─ Candidate stats                      │
│  ├─ Leave metrics                        │
│  └─ System health                        │
├──────────────────────────────────────────┤
│ MetricsDashboard class:                  │
│  ├─ Refresh interval                     │
│  ├─ Cache management                     │
│  └─ Category-based retrieval             │
└──────────────────────────────────────────┘
```

#### Design Patterns Used:
- **Utility Pattern** - Shared functions
- **Singleton Pattern** - Global logger instance
- **Factory Pattern** - Logger creation
- **Builder Pattern** - Complex export objects

---

### 8. 🔄 **Orchestration Layer** - Main Pipeline
**Role:** Coordinate all phases  
**Files:** `main.py`, `pipeline.py`, `config.py`

#### Architecture:
```
┌─────────────────────────────────────────────┐
│         MAIN ENTRY POINT (main.py)          │
├─────────────────────────────────────────────┤
│                                             │
│  Initializes:                               │
│  └─ Configuration                           │
│  └─ Logging                                 │
│  └─ All phase engines                       │
└────────────┬────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────┐
│       PIPELINE COORDINATOR (pipeline.py)    │
├─────────────────────────────────────────────┤
│                                             │
│  Orchestrates phases in sequence:           │
│  1. Resume extraction & screening           │
│  2. Interview data collection               │
│  3. Schedule generation                     │
│  4. Leave approval                          │
│  5. Escalation detection                    │
│  6. Export results                          │
│                                             │
│  State Management:                          │
│  └─ Tracks progress through pipeline        │
│  └─ Handles errors & rollback               │
│  └─ Manages dependencies                    │
└─────────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────────┐
│       CONFIGURATION LAYER (config.py)       │
├─────────────────────────────────────────────┤
│                                             │
│  Environment configuration:                 │
│  ├─ Database settings                       │
│  ├─ API keys & credentials                  │
│  ├─ Feature flags                           │
│  ├─ Policy definitions                      │
│  └─ System parameters                       │
└─────────────────────────────────────────────┘
```

---

## 🎯 OVERALL SYSTEM ARCHITECTURE

```
┌────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                      │
│  Streamlit Dashboard (6 Tabs) + CLI + REST API             │
└────────────┬───────────────────────┬──────────────┬────────┘
             │                       │              │
    ┌────────▼────────┐  ┌──────────▼────────┐   ┌─▼────────┐
    │   UI Components │  │  REST API Routes  │   │ CLI Cmds │
    └────────────────┘  └───────────────────┘   └────────┬─┘
                                                          │
┌────────────────────────────────────────────────────────▼──┐
│              ORCHESTRATION LAYER                          │
│  Pipeline Manager + Main Coordinator + Event Bus          │
└────────────┬──────────────────────────────────────────────┘
             │
    ┌────────┴─────────┬────────────┬──────────┬───────────┐
    │                  │            │          │           │
  Phase 1          Phase 3        Phase 4    Phase 6    Utils
 (Resume)       (Scheduling)   (Leave Mgmt) (Escalation)
    │                  │            │          │           │
   ┌▼──────────┐   ┌──▼─────────┐  ┌▼──────┐  ┌▼─────────┐ ┌▼────────┐
   │Question   │   │Scheduling  │  │Leave  │  │Rule      │ │Export   │
   │Bank       │   │Engine(CSP) │  │Policy │  │Engine    │ │Logging  │
   │Evaluator  │   │Conflict    │  │Engine │  │ML Class  │ │Explatn  │
   │Adaptive   │   │Analysis    │  │State  │  │Decision  │ │Metrics  │
   │Assessor   │   │            │  │Mgmt   │  │Combiner  │ │         │
   └────────┬──┘   └──┬─────────┘  └┬──────┘  └──┬───────┘ └────┬────┘
            │         │             │            │              │
            └─────────┼─────────────┼────────────┼──────────────┘
                      │             │            │
         ┌────────────▼─────────────▼────────────▼────────┐
         │    PERSISTENCE & DATA ACCESS LAYER             │
         │  Repositories + State Stores + Audit Logs      │
         └──────────────────────────────────────────────┬─┘
                                                        │
         ┌──────────────────────────────────────────────▼──┐
         │         STORAGE LAYER                          │
         │  JSON / SQLite / Memory / External APIs        │
         └──────────────────────────────────────────────────┘
```

---

## 📊 DATA FLOW EXAMPLE: Resume → Offer

```
┌─ User uploads Resume.pdf
│
├─→ Resume Extractor
│   └─ Extract text, parse sections
│
├─→ Interview Engine (Phase 1)
│   ├─ Generate adaptive questions
│   ├─ Assess skills
│   ├─ Score: 92/100 ✅
│   └─ Log: State = "Qualified"
│
├─→ Scheduling Engine (Phase 3)
│   ├─ Check interviewer availability
│   ├─ Solve scheduling CSP
│   ├─ Schedule: 2026-03-05 10:00 AM
│   └─ Log: State = "Interview Scheduled"
│
├─→ Leave Management (Phase 4)
│   ├─ Check employee leave balance
│   ├─ Apply policies
│   └─ All leave requests processed
│
├─→ Escalation Detection (Phase 6)
│   ├─ Check resume/feedback for red flags
│   ├─ No escalations ✅
│   └─ Case: Clean
│
├─→ Export Generation
│   ├─ Compile all results
│   └─ Generate JSON with all outcomes
│
└─→ Dashboard Visualization
    ├─ Show candidate ranked #1
    ├─ Show interview scheduled
    ├─ Show all decision reasoning
    └─ Download button for JSON export
```

---

## 🏛️ Design Patterns Used Throughout

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Strategy** | Scheduling (CSP vs Greedy), Leave Storage | Swap implementations |
| **State Machine** | Phase 4 Leave, Candidate journey | Workflow management |
| **Plugin/Registry** | Interview Q bank, Escalation rules | Extensibility |
| **Factory** | Loader creation, Case instantiation | Object creation |
| **Repository** | Phase 4, Phase 6 | Data abstraction |
| **Adapter** | Phase 6 API, CLI | Interface compatibility |
| **Orchestrator** | Pipeline, Escalation Service | Coordination |
| **Singleton** | Logger, Config | Single shared instance |
| **Template Method** | Scheduling pipeline | Process steps |
| **Guard Clause** | State transitions | Validation |
| **Event-Driven** | Hooks, Notifications | Loose coupling |
| **Builder** | Export objects | Complex construction |
| **Constraint Satisfaction** | Scheduling | Mathematical solving |

---

## 🎯 Architecture Strengths

✅ **Modularity** - Each phase independent, can be tested separately  
✅ **Extensibility** - Pluggable strategies throughout  
✅ **Maintainability** - Clear separation of concerns  
✅ **Testability** - Each layer can be unit tested  
✅ **Scalability** - Batch processing, caching, async ready  
✅ **Auditability** - Every action logged with reasoning  
✅ **Explainability** - Decision reasoning for each outcome  
✅ **Reliability** - Error handling, validation, guards  
✅ **Performance** - Optimized algorithms (CSP), caching  
✅ **User Experience** - Clean Streamlit interface  

---

## 🚀 How Everything Connects

1. **User uploads resume** → Resume Extractor processes it
2. **Interview Engine** evaluates candidate → Ranking score assigned
3. **Scheduling Engine** finds interview slots → Calendar optimized
4. **Leave Management** processes requests → Policies enforced
5. **Escalation Engine** monitors for issues → Cases created if needed
6. **Audit Logging** records everything → Full trail maintained
7. **Explanation Engine** generates reasoning → Interpretability provided
8. **Export Manager** packages results → JSON for judges
9. **Streamlit Dashboard** visualizes all → Professional presentation
10. **Metrics Dashboard** shows health → System KPIs tracked

**Everything is logged, explained, audited, and exportable.**

