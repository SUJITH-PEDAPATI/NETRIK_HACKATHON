"""Minimal test dashboard to verify Streamlit is working"""

import streamlit as st

st.set_page_config(page_title="Test App", layout="wide")

st.title("🤖 HR Automation Agent - Test Dashboard")
st.write("# If you can see this, Streamlit is working!")

st.success("Dashboard loaded successfully!")

# Test if utilities can be imported
st.subheader("Testing imports...")

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.export_manager import export_results
    st.success("✓ utils.export_manager loaded")
except Exception as e:
    st.error(f"✗ utils.export_manager failed: {e}")

try:
    from utils.logging_system import get_logger
    st.success("✓ utils.logging_system loaded")
except Exception as e:
    st.error(f"✗ utils.logging_system failed: {e}")

# Display basic metrics
st.header("Sample Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Candidates", 8, "+2")
with col2:
    st.metric("Scheduled Interviews", 4, "+1")
with col3:
    st.metric("Accepted Offers", 2, "0")

st.divider()

# Sample dataframe
import pandas as pd
sample_data = pd.DataFrame({
    "Candidate": ["Alice Johnson", "Bob Smith", "Carol White"],
    "Position": ["Senior Dev", "Data Analyst", "Product Manager"],
    "Score": [92, 88, 85],
    "Status": ["Qualified", "Review", "Pending"]
})

st.subheader("Recent Candidates")
st.dataframe(sample_data, width='stretch')
