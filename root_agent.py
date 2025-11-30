from google.adk.agents import (
    SequentialAgent,
    ParallelAgent,
    LlmAgent,
)
from google.adk.tools import FunctionTool
from config import config
from agents.intake_agent import intake_agent
from agents.search_agent import search_agent
from agents.legislation_agent import legislation_agent
from agents.reranking_agent import reranking_agent
from agents.composer_agent import composer_agent


def combine_search_results(google_results: list, legiscan_results: list) -> list:
    """
    Combines results from Google and LegiScan searches into a single list.
    This function ensures that the original source and description of each item
    are preserved without modification.
    """
    return google_results + legiscan_results

def create_root_agent() -> SequentialAgent:
    """Creates the root agent for the lawyer agent application."""

    # 1. Run search agents in parallel
    parallel_searcher = ParallelAgent(
        name="parallel_searcher",
        sub_agents=[search_agent, legislation_agent],
    )

    # 2. Combine the parallel search results into a single list for the next step.
    results_combiner = LlmAgent(
        name="results_combiner",
        model=config.worker_model,
        description="Combines search results from different sources into a single list.",
        instruction="""You will be given two lists: {google_results} and {legiscan_results}.
Use the `combine_search_results` tool to merge them into a single list.
Ensure that the original 'source' and 'description' for each item are preserved without modification.""",
        tools=[
            FunctionTool(combine_search_results)
            ],
        output_key="raw_results",
    )

    # 3. Define the main sequential workflow
    lawyer_agent_sequence = SequentialAgent(
        name="lawyer_agent_sequence",
        sub_agents=[
            intake_agent,
            parallel_searcher,
            results_combiner,
            reranking_agent,
            composer_agent,
        ],
    )

    return lawyer_agent_sequence

# Instantiate the agent
root_agent = create_root_agent()