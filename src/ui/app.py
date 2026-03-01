"""HR Automation Agent - Streamlit Dashboard"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add src to path BEFORE any other imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="HR Automation Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-approved {
        background-color: #d4edda;
        color: #155724;
    }
    .status-pending {
        background-color: #fff3cd;
        color: #856404;
    }
    .status-rejected {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Import utilities - add src to path for imports to work
from utils.export_manager import export_results, export_to_file
from utils.logging_system import get_logger, log_event
from utils.explanation_engine import get_decision_explanation
from utils.metrics_dashboard import get_system_metrics

logger = get_logger(__name__)

# Sidebar
with st.sidebar:
    st.title("🤖 HR Agent Control")
    
    # System Status
    st.subheader("System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Status", "🟢 Online", delta="Active")
    with col2:
        st.metric("Models", "3/3", delta="Ready")
    
    st.divider()
    
    # Configuration
    st.subheader("⚙️ Configuration")
    use_ml = st.toggle("Enable ML Classifier", value=True)
    enable_logging = st.toggle("Enable Audit Logging", value=True)
    debug_mode = st.toggle("Debug Mode", value=False)
    
    st.divider()
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    if st.button("🔄 Refresh Data", width='stretch'):
        st.rerun()
    
    if st.button("📥 Import Configuration", width='stretch'):
        st.info("Configuration import feature")
    
    if st.button("🧹 Clear Cache", width='stretch'):
        st.cache_data.clear()
        st.success("Cache cleared!")


# Main Content - Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Resume Upload",
    "🗓 Scheduling",
    "🏖 Leave Management",
    "📊 Candidate History",
    "🚨 Escalation Monitor",
    "⚙️ Settings & Export"
])


# TAB 1: Resume Upload
with tab1:
    st.header("📄 Resume Upload & Screening")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Upload Resumes")
        uploaded_files = st.file_uploader(
            "Upload resume files (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            key="resume_uploader"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
            
            for file in uploaded_files:
                st.write(f"📌 {file.name} ({file.size} bytes)")
            
            if st.button("🚀 Start Screening", key="start_screening"):
                log_event("resume_screening_started", {"file_count": len(uploaded_files)})
                st.info("Processing resumes with interview engine...")
    
    with col2:
        st.subheader("Quick Stats")
        st.metric("Files", len(uploaded_files) if uploaded_files else 0)
        st.metric("Status", "Ready")
    
    st.divider()
    
    # Ranked Candidates
    st.subheader("🏆 Ranked Candidates")
    
    sample_candidates = pd.DataFrame({
        "Rank": [1, 2, 3, 4, 5],
        "Name": ["Alice Johnson", "Bob Smith", "Carol Davis", "David Miller", "Emma Wilson"],
        "Score": [92, 88, 85, 79, 75],
        "Skills Match": ["98%", "85%", "92%", "78%", "82%"],
        "Experience": ["5 years", "3 years", "6 years", "2 years", "4 years"],
        "Status": ["Qualified", "Qualified", "Review", "Review", "Pending"],
    })
    
    # Color code scores
    def score_color(val):
        if val >= 90:
            return "background-color: #d4edda"
        elif val >= 80:
            return "background-color: #fff3cd"
        else:
            return "background-color: #f8d7da"
    
    st.dataframe(
        sample_candidates.style.applymap(score_color, subset=['Score']),
        width='stretch'
    )
    
    # Score Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            x=[92, 88, 85, 79, 75],
            nbins=10,
            title="Score Distribution",
            labels={"x": "Score", "y": "Count"}
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.pie(
            values=[2, 2, 1],
            names=["Qualified", "Review", "Pending"],
            title="Candidate Status",
            color_discrete_sequence=["#4CAF50", "#FFC107", "#F44336"]
        )
        st.plotly_chart(fig, width='stretch')


# TAB 2: Scheduling
with tab2:
    st.header("🗓 Interview Scheduling")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Schedule Calendar")
        
        # Date selection
        selected_date = st.date_input("Select date range", value=datetime.now())
        
        # Sample schedule
        schedule_data = {
            "Date": ["2026-03-05", "2026-03-05", "2026-03-06", "2026-03-06"],
            "Time": ["10:00 AM", "2:00 PM", "11:00 AM", "3:00 PM"],
            "Candidate": ["Alice Johnson", "Bob Smith", "Carol Davis", "David Miller"],
            "Interviewer": ["John Doe", "Jane Smith", "Mike Brown", "Sarah Lee"],
            "Status": ["Scheduled", "Scheduled", "Pending", "Confirmed"],
            "Duration": ["1 hour", "45 min", "1 hour", "1 hour"]
        }
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, width='stretch')
    
    with col2:
        st.subheader("📊 Scheduling Stats")
        st.metric("Total Scheduled", 4)
        st.metric("Confirmed", 1)
        st.metric("Pending", 1)
        st.metric("Conflicts", 0)
    
    st.divider()
    
    # Scheduling Calendar View
    st.subheader("📅 Calendar View")
    
    # Simple calendar visualization
    calendar_data = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Interviews": [2, 3, 1, 2, 1, 0, 0],
    }
    
    fig = px.bar(
        x=calendar_data["Day"],
        y=calendar_data["Interviews"],
        title="Interviews per Day",
        labels={"x": "Day", "y": "Count"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Add Interview
    st.subheader("➕ Schedule New Interview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        candidate = st.selectbox("Select Candidate", ["Alice Johnson", "Bob Smith", "Carol Davis"])
    with col2:
        interview_date = st.date_input("Interview Date")
    with col3:
        interview_time = st.time_input("Interview Time")
    
    if st.button("📅 Add to Schedule"):
        log_event("interview_scheduled", {
            "candidate": candidate,
            "date": str(interview_date),
            "time": str(interview_time)
        })
        st.success(f"✅ Interview scheduled for {candidate}")


# TAB 3: Leave Management
with tab3:
    st.header("🏖 Leave Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Leave Balance", "21 days", delta="+1.75/month")
    with col2:
        st.metric("Used Days", "5 days", delta="24%")
    with col3:
        st.metric("Remaining Days", "16 days", delta="76%")
    
    st.divider()
    
    # Leave Request Form
    st.subheader("📝 Submit Leave Request")
    
    col1, col2 = st.columns(2)
    
    with col1:
        leave_type = st.selectbox(
            "Leave Type",
            ["Annual", "Sick", "Maternity", "Paternity", "Unpaid"]
        )
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
    
    with col2:
        reason = st.text_area("Reason", height=100)
        notification_contact = st.text_input("Contact During Leave")
    
    if st.button("📤 Submit Request"):
        duration = (end_date - start_date).days + 1
        log_event("leave_request_submitted", {
            "leave_type": leave_type,
            "duration": duration,
            "reason": reason
        })
        st.success(f"✅ Leave request submitted for {duration} days")
    
    st.divider()
    
    # Leave History
    st.subheader("📊 Leave History")
    
    leave_history = pd.DataFrame({
        "Date Range": ["2026-02-01 to 2026-02-05", "2026-01-20 to 2026-01-22"],
        "Type": ["Annual Leave", "Sick Leave"],
        "Days": [5, 3],
        "Status": ["Approved ✅", "Approved ✅"],
        "Approval Details": ["Approved by John Doe", "Auto-approved"],
    })
    
    st.dataframe(leave_history, width='stretch')
    
    st.divider()
    
    # Leave Decision Reasoning
    st.subheader("💡 Decision Reasoning")
    
    if st.button("Show Decision Logic"):
        explanation = get_decision_explanation("leave_request", {
            "leave_type": "Annual",
            "duration": 5,
            "balance": 16
        })
        
        with st.expander("🔍 Decision Process", expanded=True):
            st.write(explanation)


# TAB 4: Candidate History & State Transitions
with tab4:
    st.header("📊 Candidate History & State Transitions")
    
    # Select candidate
    candidate = st.selectbox("Select Candidate", [
        "Alice Johnson",
        "Bob Smith",
        "Carol Davis",
        "David Miller",
        "Emma Wilson"
    ])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Candidate Profile")
        
        profile_data = {
            "Name": candidate,
            "Overall Score": 92,
            "Application Date": "2026-02-28",
            "Current Status": "Interview Scheduled",
            "Skills Match": "98%",
            "Experience": "5 years",
        }
        
        for key, value in profile_data.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.subheader("📌 Quick Info")
        st.metric("Applications", 1)
        st.metric("Interviews", 1)
        st.metric("Score", 92)
    
    st.divider()
    
    # State Transition History
    st.subheader("🔄 State Transition History")
    
    transitions = pd.DataFrame({
        "Timestamp": [
            "2026-02-28 10:00 AM",
            "2026-02-28 02:30 PM",
            "2026-03-01 09:00 AM",
            "2026-03-02 11:30 AM",
        ],
        "From State": [
            "Submitted",
            "Screening",
            "Qualified",
            "Interview Scheduled"
        ],
        "To State": [
            "Screening",
            "Qualified",
            "Interview Scheduled",
            "Interview Scheduled"
        ],
        "Trigger": [
            "Auto Submit",
            "Resume Analysis",
            "Score >= 85",
            "Calendar Slot Found"
        ],
        "Duration": [
            "4h 30m",
            "6h 30m",
            "2h",
            "In Progress"
        ]
    })
    
    st.dataframe(transitions, width='stretch')
    
    # Timeline Visualization
    st.subheader("📅 Timeline")
    
    timeline_fig = go.Figure()
    
    states = ["Submitted", "Screening", "Qualified", "Interview Scheduled"]
    dates = ["2026-02-28", "2026-02-28", "2026-03-01", "2026-03-02"]
    
    timeline_fig.add_trace(go.Scatter(
        x=dates,
        y=states,
        mode='markers+lines',
        marker=dict(size=15, color="RoyalBlue"),
        line=dict(width=3),
        name=candidate
    ))
    
    timeline_fig.update_layout(
        title=f"State Transition Timeline - {candidate}",
        xaxis_title="Date",
        yaxis_title="State",
        height=400,
        hovermode="closest"
    )
    
    st.plotly_chart(timeline_fig, use_container_width=True)


# TAB 5: Escalation Monitor
with tab5:
    st.header("🚨 Escalation Monitor")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 Critical", 1, delta="-1")
    with col2:
        st.metric("🟠 High", 3, delta="+2")
    with col3:
        st.metric("🟡 Medium", 5, delta="=")
    with col4:
        st.metric("🟢 Low", 8, delta="+3")
    
    st.divider()
    
    # Active Escalations
    st.subheader("📋 Active Escalations")
    
    escalations = pd.DataFrame({
        "Case ID": ["ESC-001", "ESC-002", "ESC-003", "ESC-004"],
        "Category": ["Legal", "Harassment", "Fraud", "Compliance"],
        "Severity": ["🔴 Critical", "🟠 High", "🟠 High", "🟡 Medium"],
        "Status": ["Open", "Under Investigation", "Open", "Pending Review"],
        "Assigned To": ["HR Manager", "Legal Team", "Compliance", "HR Manager"],
        "Created": ["2026-03-01", "2026-02-28", "2026-02-27", "2026-02-26"],
        "Age": ["1 day", "3 days", "4 days", "5 days"]
    })
    
    st.dataframe(escalations, width='stretch')
    
    st.divider()
    
    # Escalation Details
    st.subheader("🔍 Escalation Details")
    
    case_id = st.selectbox("Select Case", escalations["Case ID"].tolist())
    
    if case_id:
        with st.expander(f"Details: {case_id}", expanded=True):
            st.write("**Description:** Employee reported potential harassment in workplace.")
            st.write("**Trigger Keywords:** Detected 'harassment', 'hostile', 'discrimination'")
            st.write("**Confidence:** 87%")
            st.write("**Recommended Actions:** Interview, Documentation Review, Investigation")
            
            if st.button("🔗 View Full Case"):
                st.info("Full case details loading...")
    
    # Escalation Trends
    st.subheader("📈 Escalation Trends")
    
    trend_data = {
        "Date": pd.date_range("2026-02-01", periods=10, freq="D"),
        "New Escalations": [2, 1, 3, 2, 4, 1, 2, 3, 1, 2],
        "Resolved": [0, 2, 1, 2, 1, 3, 2, 1, 2, 1]
    }
    
    trend_df = pd.DataFrame(trend_data)
    
    fig = px.line(
        trend_df,
        x="Date",
        y=["New Escalations", "Resolved"],
        title="Escalation Trends",
        markers=True
    )
    
    st.plotly_chart(fig, width='stretch')


# TAB 6: Settings & Export
with tab6:
    st.header("⚙️ Settings & Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 System Metrics")
        
        metrics = get_system_metrics()
        
        for metric_name, metric_value in metrics.items():
            st.metric(metric_name, metric_value)
    
    with col2:
        st.subheader("🔧 Configuration")
        
        enable_ml = st.toggle("ML Classifier", value=True)
        enable_logging = st.toggle("Audit Logging", value=True)
        enable_notifications = st.toggle("Notifications", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved")
    
    st.divider()
    
    # Export Results
    st.subheader("📤 Export Results")
    
    st.write("Generate standardized JSON export with all system outputs.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Generate Export", key="export_btn"):
            try:
                results = export_results()
                
                st.success("✅ Export generated successfully!")
                
                # Display summary
                st.write("**Export Summary:**")
                st.metric("Ranked Candidates", len(results.get("rankings", [])))
                st.metric("Scheduled Interviews", len(results.get("interviews", [])))
                st.metric("Leave Decisions", len(results.get("leave_decisions", [])))
                st.metric("State Logs", len(results.get("state_logs", [])))
                
                # Download button
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_str,
                    file_name=f"hr_automation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                # Preview
                with st.expander("👀 Preview Export"):
                    st.json(results)
                
                log_event("export_generated", {"timestamp": datetime.now().isoformat()})
                
            except Exception as e:
                st.error(f"❌ Export failed: {str(e)}")
    
    with col2:
        export_format = st.selectbox("Export Format", ["JSON", "CSV", "PDF"])
        
        if st.button("📁 Export as " + export_format):
            st.info(f"Exporting as {export_format}...")
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    st.divider()
    
    # System Logs
    st.subheader("📋 System Logs")
    
    if st.button("View Latest Logs"):
        st.info("Loading recent system logs...")
        
        # Sample logs
        logs = [
            {"timestamp": "2026-03-02 14:30:15", "level": "INFO", "message": "Resume screening completed", "event": "resume_screening_completed"},
            {"timestamp": "2026-03-02 14:20:30", "level": "INFO", "message": "Interview scheduled", "event": "interview_scheduled"},
            {"timestamp": "2026-03-02 14:10:45", "level": "WARNING", "message": "High escalation detected", "event": "escalation_detected"},
            {"timestamp": "2026-03-02 13:50:20", "level": "INFO", "message": "Leave request approved", "event": "leave_approved"},
        ]
        
        logs_df = pd.DataFrame(logs)
        st.dataframe(logs_df, width='stretch')


# Footer
st.divider()
st.markdown("""
---
**HR Automation Agent** | Built for Netrik Hackathon 2026
- 🏆 Multi-phase intelligent automation system
- 📊 Real-time monitoring and reporting
- 🔒 Audit logging and compliance tracking
- ✨ Advanced decision explanation engine
""")
