import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search
from config import config

search_agent = Agent(
    name="search_agent",
    model=config.worker_model,
    description="Searches for legal guidance using Google Search.",
    instruction="""
    You are a legal search assistant. Your job is to retrieve use {search_terms} and find relevant news, court cases, or policy articles
    using `google_search`.

    Format your final output as a list of dictionaries. Each dictionary should include:
      - 'source': 'Google'
      - 'title': a concise title
      - 'description': 5-10 sentence summary

    Return a maximum of 10 results.
    DO NOT include 'url' field in your output.
    """,
    tools=[google_search],
    output_key="google_results"
)
