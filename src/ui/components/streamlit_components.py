"""Reusable Streamlit components."""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional


def metric_card(title: str, value: str, delta: Optional[str] = None, icon: str = ""):
    """Display a metric card."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(title, value, delta=delta)
    with col2:
        st.write(f"## {icon}")


def status_badge(status: str, status_map: Dict[str, str] = None):
    """Display a status badge."""
    if status_map is None:
        status_map = {
            "approved": "🟢 Approved",
            "pending": "🟡 Pending",
            "rejected": "🔴 Rejected",
            "scheduled": "🔵 Scheduled",
            "completed": "✅ Completed",
        }
    
    return status_map.get(status.lower(), status)


def data_table(df: pd.DataFrame, title: str = "", highlight_cols: List[str] = None):
    """Display a formatted data table."""
    if title:
        st.subheader(title)
    
    st.dataframe(df, use_container_width=True)


def progress_section(current: int, total: int, label: str = ""):
    """Display progress bar."""
    progress = current / total if total > 0 else 0
    st.progress(progress)
    if label:
        st.caption(f"{label}: {current}/{total}")


def info_box(title: str, content: str, icon: str = "ℹ️"):
    """Display info box."""
    st.info(f"**{icon} {title}**\n\n{content}")


def warning_box(title: str, content: str, icon: str = "⚠️"):
    """Display warning box."""
    st.warning(f"**{icon} {title}**\n\n{content}")


def success_box(title: str, content: str, icon: str = "✅"):
    """Display success box."""
    st.success(f"**{icon} {title}**\n\n{content}")


def error_box(title: str, content: str, icon: str = "❌"):
    """Display error box."""
    st.error(f"**{icon} {title}**\n\n{content}")


def expandable_section(title: str, content_func, expanded: bool = False):
    """Create expandable section."""
    with st.expander(title, expanded=expanded):
        content_func()


def two_column_comparison(left_title: str, left_content, right_title: str, right_content):
    """Display two-column comparison."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(left_title)
        st.write(left_content)
    
    with col2:
        st.subheader(right_title)
        st.write(right_content)
