"""
Session Service Configuration
Manages session storage for the Lawyer Agent application
"""
from google.adk.sessions import InMemorySessionService

# Application configuration
APP_NAME = "lawyer_agent"
USER_ID = "default"

# Initialize the session service
# InMemorySessionService stores conversations in RAM (temporary)
session_service = InMemorySessionService()

print(f"Session service initialized: {session_service.__class__.__name__}")
