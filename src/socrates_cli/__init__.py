"""
Socrates CLI - Command-line interface for Socrates AI framework.

Provides a comprehensive set of commands for:
- Project management
- Code analysis and generation
- Conversation and sessions
- Collaboration
- Analytics and maturity tracking
- Document management
- Workflow orchestration
"""

__version__ = "0.1.0"
__author__ = "Socrates Team"
__email__ = "info@socrates-ai.dev"

from socrates_cli.commands import (
    # Analytics commands
    AnalyticsAnalyzeCommand,
    AnalyticsBreakdownCommand,
    AnalyticsRecommendCommand,
    AnalyticsStatusCommand,
    AnalyticsSummaryCommand,
    AnalyticsTrendsCommand,
    # Code commands
    CodeDocsCommand,
    CodeExplainCommand,
    CodeGenerateCommand,
    CodeReviewCommand,
    # Collaboration commands
    CollabAddCommand,
    CollabListCommand,
    CollabRemoveCommand,
    CollabRoleCommand,
    # Conversation commands
    ConvSearchCommand,
    ConvSummaryCommand,
    # Session commands
    SessionCreateCommand,
    SessionDeleteCommand,
    SessionExportCommand,
    SessionImportCommand,
    SessionListCommand,
    SessionLoadCommand,
    SessionSaveCommand,
    SessionSwitchCommand,
    # And more...
)

__all__ = [
    "AnalyticsAnalyzeCommand",
    "AnalyticsBreakdownCommand",
    "AnalyticsRecommendCommand",
    "AnalyticsStatusCommand",
    "AnalyticsSummaryCommand",
    "AnalyticsTrendsCommand",
    "CodeDocsCommand",
    "CodeExplainCommand",
    "CodeGenerateCommand",
    "CodeReviewCommand",
    "CollabAddCommand",
    "CollabListCommand",
    "CollabRemoveCommand",
    "CollabRoleCommand",
    "ConvSearchCommand",
    "ConvSummaryCommand",
    "SessionCreateCommand",
    "SessionDeleteCommand",
    "SessionExportCommand",
    "SessionImportCommand",
    "SessionListCommand",
    "SessionLoadCommand",
    "SessionSaveCommand",
    "SessionSwitchCommand",
]
