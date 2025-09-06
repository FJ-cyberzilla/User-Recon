# user_recon/__init__.py

"""
User Recon - Advanced OSINT & AI Analysis Toolkit
-------------------------------------------------
An intelligent reconnaissance tool that scans social platforms,
applies AI pattern recognition, entropy analysis, anomaly detection,
and predictive reasoning to identify username similarities across the web.
"""

__version__ = "1.0.0"
__author__ = "User Recon Project"
__license__ = "MIT"

# Expose core functionality
from .core.search import search_username
from .core.ai_compare import compare_usernames
from .core.patterns import PatternAnalyzer
from .core.security import SecurityManager

# Utility imports
from .utils.entropy import calculate_entropy
from .utils.telemetry import Telemetry
from .utils.logging import get_logger

# Make package logger available everywhere
logger = get_logger("user_recon")

__all__ = [
    "search_username",
    "compare_usernames",
    "PatternAnalyzer",
    "SecurityManager",
    "calculate_entropy",
    "Telemetry",
    "logger",
]
