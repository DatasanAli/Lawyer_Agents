import datetime
from google.adk.agents import Agent
from config import config

reranking_agent = Agent(
    name="reranking_agent",
    model=config.reasoning_model,
    description="Reranks raw search results based on user query relevance, recency, and legal impact.",
    instruction="""
    You will be given:
    {search_terms} legal terms from the user's query. Look at 'search_terms' for relevance when applying the re-ranking 
    {raw_results}: a list of legal documents or articles returned by prior search tools

    Your job is to select and rerank the **top 5 most helpful results** based on:
    - Relevance to the user's question -> which is search_terms)
    - Clarity and usefulness of the results
    - Legal authority and trustworthiness
    

    For each of the top 5, output a dictionary with:
    - 'source': 'LegiScan' or 'Google'
    - 'title': concise summary title
    - 'description': 3-5 sentence explanation of its value

    DO NOT include 'url' field in your output.
    Only use the content from raw_results and search_terms to perform re-ranking. 
    DO NOT fabricate legal sources.
    
    Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}.
    """,
    output_key="top_5_results"
)
