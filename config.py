import os
from dataclasses import dataclass
import google.generativeai as genai

# Ensure default ADK config values (these can be overridden via .env)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "lawyer-agents")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

@dataclass
class ResearchConfiguration:
    """Configuration for model selection."""
    worker_model: str = "gemini-2.5-flash"
    reasoning_model: str = "gemini-2.5-pro"

config = ResearchConfiguration()
