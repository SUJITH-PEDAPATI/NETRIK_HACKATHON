# Phase 3: Advanced Conflict-Aware Interview Scheduling

⚡ **Production-Grade Scheduling Engine for High-Volume Interview Coordination**

## Overview

Phase 3 transforms the HR Automation Agent from candidate evaluation to intelligent interview scheduling. It automatically coordinates hundreds of interview slots while resolving conflicts, optimizing load distribution, and maintaining scheduling constraints.

### Quick Features

- ✅ **Multiple Algorithms**: CSP solver, Greedy heuristics, Hybrid approach
- ✅ **Conflict Detection**: Real-time conflict identification & resolution suggestions
- ✅ **Multi-Format Loading**: JSON, CSV, direct pipeline integration
- ✅ **Advanced Analytics**: Load balancing, time distribution, bottleneck analysis
- ✅ **Calendar Export**: iCalendar format for Outlook, Google Calendar, Apple Calendar
- ✅ **HTML Reports**: Interactive visualizations of schedules
- ✅ **Performance Optimized**: Scales to 1000+ candidates/interviewers

---

## Architecture

```
phase3_scheduling/
│
├── scheduling_pipeline.py        ← ENTRY POINT
│   └── Main orchestrator with CLI & advanced configuration
│
├── core/                          ← Algorithms & Logic
│   ├── scheduler.py              (CSP, Greedy, Hybrid algorithms)
│   ├── csp_solver.py             (Constraint satisfaction)
│   ├── greedy_solver.py          (Fast approximation)
│   └── conflict_analysis.py      (Conflict detection)
│
├── loaders/                       ← Data Import
│   ├── availability_loader.py    (Core loading)
│   ├── csv_loader.py             (CSV parsing)
│   ├── json_loader.py            (JSON parsing)
│   └── pipeline_bridge.py        (Phase 1-2 integration)
│
├── reporting/                     ← Output Generation
│   ├── schedule_reporter.py      (Reports & analytics)
│   └── ical_exporter.py          (Calendar export)
│
└── models/                        ← Data Structures
    ├── types.py                  (Dataclasses, enums)
    └── schema.py                 (Validation schemas)
```

---

## Usage

### 1️⃣ Command-Line Interface

```bash
# Generate random test data
python -m phase3_scheduling.scheduling_pipeline --random 20 5 --algorithm hybrid

# Load from JSON file
python -m phase3_scheduling.scheduling_pipeline --json candidates.json

# Load from CSV files
python -m phase3_scheduling.scheduling_pipeline --csv candidates.csv interviewers.csv

# Print sample JSON template
python -m phase3_scheduling.scheduling_pipeline --sample > input.json
```

### 2️⃣ Programmatic Usage

```python
from phase3_scheduling.scheduling_pipeline import run_scheduling, SchedulingConfig
from phase3_scheduling.loaders.availability_loader import generate_random

# Generate test data
matrix = generate_random(num_candidates=50, num_interviewers=10, days=10)

# Configure scheduling
config = SchedulingConfig()
config.optimization_method = "hybrid"  # or "csp" or "greedy"

# Run scheduling
result = run_scheduling(
    matrix,
    output_dir="./schedules",
    html=True,
    ical=True,
    config=config
)

# Access results
schedule = result["schedule"]
conflicts = result["conflict_report"]
analytics = result["analytics"]
```

### 3️⃣ Pipeline Bridge (Phase 1-2 Integration)

```python
from phase3_scheduling.scheduling_pipeline import run_from_pipeline

# After Phase 1-2 produce ranked candidates
ranked_candidates = [
    {"id": "C001", "name": "Jane Doe", "score": 0.92, "skills": ["Python", "AWS"]},
    {"id": "C002", "name": "John Smith", "score": 0.88, "skills": ["Java", "GCP"]},
]

interviewer_data = {
    "interviewers": [
        {"id": "I001", "name": "Alice", "available_times": ["09:00-12:00", "14:00-17:00"]},
        {"id": "I002", "name": "Bob", "available_times": ["10:00-13:00", "15:00-18:00"]},
    ]
}

result = run_from_pipeline(
    ranked_results=ranked_candidates,
    interviewers_data=interviewer_data,
    start_date="2026-03-10",
    days=5,
)
```

---

## Algorithms

### 🔵 Constraint Satisfaction Problem (CSP)

**Best for**: Optimal solutions, small to medium datasets
- Backtracking with constraint propagation
- Finds globally optimal schedule
- Slower but guarantees best solution
- Good for <100 candidates

**Use**: `--algorithm csp`

### 🟢 Greedy Algorithm

**Best for**: Speed, large datasets
- Sorts candidates by priority
- Assigns each to best available slot
- O(n log n) complexity
- Fast, near-optimal results
- Good for 100+ candidates

**Use**: `--algorithm greedy`

### 🟡 Hybrid Approach (Default)

**Best for**: Balance of speed and quality
- Starts with greedy solution
- Refines with CSP constraints
- Combines strengths of both
- Best overall performance
- Recommended for most cases

**Use**: `--algorithm hybrid` (default)

---

## Scheduling Constraints

### Hard Constraints (Must satisfy)
- ✓ No interviewer double-booking
- ✓ No candidate conflicts
- ✓ Respect availability windows
- ✓ Maximum interviews per interviewer per day

### Soft Constraints (Optimized)
- ⚡ Candidates prefer morning/afternoon times
- ⚡ Skill-interviewer matching bonus
- ⚡ Balanced interviewer load
- ⚡ Even distribution across days

---

## Conflict Detection

The system automatically identifies 5 types of conflicts:

### 1. **Time Conflicts** (CRITICAL)
```
❌ Interviewer I001 double-booked:
   • 09:00-10:00: Candidate A
   • 09:30-10:30: Candidate B
```

### 2. **Interviewer Overload** (HIGH)
```
⚠️  Interviewer I001 scheduled for 6 interviews in 1 day (max: 5)
```

### 3. **Tight Scheduling** (MEDIUM)
```
⚠️  Candidate C001 has only 0.5h gap between interviews
```

### 4. **Unscheduled Candidates** (HIGH)
```
❌ 3 candidates could not be scheduled
```

### 5. **Skill Mismatches** (LOW)
```
⚠️  Candidate Python expert matched with Java interviewer
```

---

## Output Generation

### JSON Schedule
```json
{
  "interviews": [
    {
      "candidate_id": "C001",
      "candidate_name": "Jane Doe",
      "interviewer_id": "I001",
      "start_time": "2026-03-10T09:00:00",
      "end_time": "2026-03-10T10:00:00",
      "duration_minutes": 60
    }
  ],
  "stats": {
    "scheduled_count": 45,
    "total_variables": 50,
    "unscheduled_count": 5,
    "success_rate": 90.0,
    "solver_time_seconds": 2.34
  }
}
```

### HTML Report
- Interactive table of all interviews
- Candidate and interviewer views
- Statistics dashboard
- Exportable for stakeholders

### iCalendar (.ics)
- Import directly into Outlook/Google Calendar/Apple Calendar
- Automatic reminders
- Per-candidate or per-interviewer calendars

---

## Analytics Dashboard

### Load Distribution
```
Interviewer Load:
  I001: 8 interviews  ████████
  I002: 7 interviews  ███████
  I003: 5 interviews  █████
  Average: 6.7 interviews/day
```

### Time Distribution
```
Peak Hours:
  09:00 - 10:00: 12 interviews (14%)
  10:00 - 11:00: 15 interviews (18%)
  14:00 - 15:00: 13 interviews (15%)
```

### Success Metrics
```
Scheduling Success: 90%
  • Scheduled: 45/50 candidates
  • Conflicts: 0 critical, 2 warnings
  • Execution Time: 2.34 seconds
  • Slot Utilization: 73%
```

---

## Configuration

```python
class SchedulingConfig:
    optimization_method = "hybrid"      # "csp", "greedy", "hybrid"
    max_iterations = 1000               # CSP max depth
    allow_conflicts = False             # Force scheduling even with conflicts
    conflict_resolution_strategy = "reschedule"  # How to resolve conflicts
    report_formats = ["json", "html", "ical"]   # Output formats
    performance_tracking = True         # Track metrics
```

---

## Data Format

### Required Input

```json
{
  "candidates": [
    {
      "id": "C001",
      "name": "Jane Doe",
      "email": "jane@example.com",
      "preferred_times": ["09:00-12:00", "14:00-17:00"],
      "unavailable_dates": ["2026-03-15"],
      "skills": ["Python", "AWS"],
      "rounds_needed": 2,
      "seniority": "mid"
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
      "max_per_day": 4
    }
  ],
  "date_range": {
    "start_date": "2026-03-10",
    "end_date": "2026-03-15"
  }
}
```

---

## Performance

| Metric | Value |
|--------|-------|
| Candidate Scaling | 0-1000+ |
| Interviewer Scaling | 0-100+ |
| Algorithm | Time |
| CSP (50 candidates) | 2-5 seconds |
| Greedy (500 candidates) | 0.1-0.3 seconds |
| Hybrid (200 candidates) | 0.5-1.2 seconds |

---

## Error Handling

```python
try:
    result = run_scheduling(matrix)
    if result["success"]:
        print("✅ Scheduling successful")
    else:
        print("❌ Error occurred")
        print(result["errors"])
except ValueError as e:
    print(f"Data validation error: {e}")
except Exception as e:
    print(f"Scheduling failed: {e}")
```

---

## Roadmap

- [ ] Machine Learning-based slot recommendation
- [ ] Automatic conflict resolution
- [ ] Email notifications to candidates
- [ ] Video conferencing integration
- [ ] Feedback loop optimization
- [ ] Multi-round coordinated scheduling
- [ ] Geographic timezone awareness

---

## Support

For issues or questions:
1. Check logs in `output/` directory
2. Validate input data format
3. Try different algorithm (`--algorithm greedy` for first attempt)
4. Review HTML report for visualization of conflicts

