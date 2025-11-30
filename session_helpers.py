"""
Session Helper Functions
Provides utilities for managing conversation sessions with the Lawyer Agent
"""
from google.genai import types
from google.adk.runners import Runner
from session_service import session_service, USER_ID


async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    """
    Manages a complete conversation session, handling session creation/retrieval,
    query processing, and response streaming.

    Args:
        runner_instance: The Runner instance managing the agent
        user_queries: Single query string or list of query strings to process
        session_name: Unique identifier for this session

    Example:
        >>> await run_session(runner, "What is contract law?", "legal-session")
        >>> await run_session(runner, ["Hello!", "Explain tort law"], "intro-session")
    """
    print(f"\n### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
        print(f"New session created: {session_name}")
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
        print(f"Retrieved existing session: {session_name}")

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query_content = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query_content
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"Agent > {event.content.parts[0].text}")
    else:
        print("No queries provided!")


print("Session helper functions loaded")
