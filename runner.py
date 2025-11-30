import asyncio
import warnings
from dotenv import load_dotenv

# Load environment variables before importing root_agent
load_dotenv()

# Suppress Google Auth warnings about quota project
warnings.filterwarnings("ignore", message=".*Your application has authenticated using end user credentials.*")

from google.adk.runners import Runner
from root_agent import root_agent
from session_service import session_service, APP_NAME, USER_ID
from session_helpers import run_session


async def interactive_mode():
    """
    Interactive mode: Continuous conversation loop with the agent.
    Uses the session service to maintain conversation history.
    """
    print("Starting Lawyer Agent Interactive Session...")
    print("Type 'exit' or 'quit' to end the session.\n")

    # Create runner with session service
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Use run_session for maintaining context
    session_name = "interactive-session"

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_name
        )

    try:
        while True:
            user_input = input("User > ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Ending session.")
                break

            if not user_input:
                continue

            # Run the query using the helper function
            await run_session(runner, user_input, session_name)

    except (KeyboardInterrupt, EOFError):
        print("\nEnding session.")


async def main():
    """
    Main entry point - you can switch between modes
    """
    # Option 1: Use interactive mode (recommended)
    await interactive_mode()

    # Option 2: Use session-based queries (for programmatic usage)
    # runner = Runner(
    #     agent=root_agent,
    #     app_name=APP_NAME,
    #     session_service=session_service
    # )
    # await run_session(
    #     runner,
    #     ["What is contract law?", "Give me an example"],
    #     "legal-consultation-1"
    # )


if __name__ == "__main__":
    asyncio.run(main())
