"""Dashboard configuration and initialization."""

import os
import json
from pathlib import Path
from datetime import datetime


class DashboardConfig:
    """Dashboard configuration manager."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config = {
            "app_name": "HR Automation Agent",
            "version": "1.0.0",
            "environment": os.getenv("ENV", "development"),
            "debug": os.getenv("DEBUG", "false").lower() == "true",
            "theme": "light",
            "layout": "wide",
            "refresh_interval_seconds": 30,
            
            # Feature flags
            "features": {
                "resume_upload": True,
                "interview_scheduling": True,
                "leave_management": True,
                "candidate_history": True,
                "escalation_monitor": True,
                "export_results": True,
                "analytics_dashboard": True,
                "ml_classifier": True,
                "audit_logging": True
            },
            
            # Performance settings
            "performance": {
                "cache_ttl_seconds": 300,
                "max_batch_size": 100,
                "worker_threads": 4,
                "timeout_seconds": 30
            },
            
            # UI settings
            "ui": {
                "sidebar_state": "expanded",
                "tabs": [
                    "📄 Resume Upload",
                    "🗓 Scheduling",
                    "🏖 Leave Management",
                    "📊 Candidate History",
                    "🚨 Escalation Monitor",
                    "⚙️ Settings & Export"
                ],
                "enable_dark_mode": False,
                "show_metrics": True,
                "show_logs": True
            },
            
            # Export settings
            "export": {
                "format": "json",
                "include_audit_logs": True,
                "include_metrics": True,
                "include_explanations": True,
                "pretty_print": True,
                "compression": "none"  # gzip, none
            },
            
            # Logging settings
            "logging": {
                "level": "INFO",
                "format": "json",
                "output_dir": "logs",
                "retention_days": 30,
                "enable_rotation": True,
                "max_size_mb": 100
            },
            
            # Database/Storage settings
            "storage": {
                "type": "json",  # json, sqlite, postgresql
                "path": "data"
            }
        }
        
        self._create_directories()
        self._load_from_env()
    
    def _create_directories(self):
        """Create necessary directories."""
        Path(self.config["logging"]["output_dir"]).mkdir(exist_ok=True)
        Path(self.config["storage"]["path"]).mkdir(exist_ok=True)
        Path("exports").mkdir(exist_ok=True)
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Override with environment variables if present
        if os.getenv("DEBUG"):
            self.config["debug"] = os.getenv("DEBUG").lower() == "true"
        
        if os.getenv("THEME"):
            self.config["ui"]["enable_dark_mode"] = os.getenv("THEME") == "dark"
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, {})
            else:
                return default
        
        return value if value != {} else default
    
    def set(self, key: str, value):
        """Set configuration value."""
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        
        config[keys[-1]] = value
    
    def save_to_file(self, filepath: str = "config.json"):
        """Save configuration to file."""
        with open(filepath, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def load_from_file(self, filepath: str = "config.json"):
        """Load configuration from file."""
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.config.update(json.load(f))
    
    def to_dict(self):
        """Export configuration as dictionary."""
        return self.config.copy()


# Global configuration instance
_dashboard_config = None


def get_dashboard_config() -> DashboardConfig:
    """Get global dashboard configuration."""
    global _dashboard_config
    
    if _dashboard_config is None:
        _dashboard_config = DashboardConfig()
    
    return _dashboard_config


def init_dashboard():
    """Initialize dashboard."""
    config = get_dashboard_config()
    
    # Create logs directory
    Path(config.get("logging.output_dir")).mkdir(exist_ok=True)
    
    # Initialize logging
    from utils.logging_system import get_logger
    logger = get_logger("dashboard")
    logger.log_event("dashboard_initialized", {
        "timestamp": datetime.now().isoformat(),
        "config_version": config.get("version")
    })
    
    return config
