import os
import requests
from typing import List, Dict, Optional
from google.adk.tools import FunctionTool

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
LEGISCAN_BASE_URL = "https://api.legiscan.com/"

def search_legiscan_bills(query: str, state: str = "CA") -> List[Dict]:
    """
    Search LegiScan for relevant bills based on legal search terms.

    Args:
        query (str): Legal search terms (e.g. "tenant rights mold").
        state (str): Two-letter state abbreviation.

    Returns:
        List[Dict]: A list of bill summaries.
    """
    if not LEGISCAN_API_KEY:
        raise EnvironmentError("LEGISCAN_API_KEY not found in environment variables.")

    params = {
        "key": LEGISCAN_API_KEY,
        "op": "getSearch",
        "state": state,
        "query": query
    }

    try:
        response = requests.get(LEGISCAN_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for k, bill in data.get("searchresult", {}).items():
            if k == "summary":
                continue
            results.append({
                "source": "LegiScan",
                "title": bill.get("title"),
                "description": bill.get("description"),
            })

        return results[:10]  # limit to top 10

    except Exception as e:
        return [{"source": "LegiScan", "title": "Error", "description": str(e)}]


# Export ADK-compatible FunctionTool
search_legiscan_bills_tool = FunctionTool(search_legiscan_bills)
