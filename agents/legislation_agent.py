import datetime
from google.adk.agents import Agent
 
from config import config
from tools.legiscan_tool import search_legiscan_bills_tool

legislation_agent = Agent(
    name="legislation_agent",
    model=config.worker_model,
    description="Searches for legal guidance using the LegiScan tool.",
    instruction="""
    You are a legislative search assistant. Your job is to search using {search_terms} and find retrieve relevant laws and bills
    using the `search_legiscan_bills_tool`.

    Format your final output as a list of dictionaries. Each dictionary should include:
      - 'source': 'LegiScan'
      - 'title': a concise title
      - 'description': 5-10 sentence summary

    Return a maximum of 10 results.
    DO NOT include 'url' field in your output.
    """,
    tools=[search_legiscan_bills_tool],
    output_key="legiscan_results",
)