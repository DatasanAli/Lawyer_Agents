import datetime
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
 
from config import config
from tools.query_standardizer import standardize_legal_query

intake_agent = Agent(
    name="intake_agent",
    model=config.worker_model,
    description="Extracts key legal search terms from a user's inquiry.",
    instruction="""
    You are a legal query interpreter.
    Your job is to convert a user's legal question into standardized, keyword-based search terms.

    Steps:
    1. Call the `standardize_legal_query` tool with the user's query
    2. Return ONLY the list of keywords that the tool provides (e.g., ["model", "landlord", "rights"])

    Do not return the original query. Only return the standardized search terms.
    """,
    tools=[
        FunctionTool(standardize_legal_query),
    ],
    output_key="search_terms",
)
