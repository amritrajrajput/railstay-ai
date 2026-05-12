import os
import logging
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from agent.planner import SearchPlanner
from agent.ranking import ResultRanker
from tools.irctc_search import IRCTCSearchTool
import concurrent.futures

logger = logging.getLogger(__name__)

# 1️⃣ Define the State our Agent will pass between nodes
class AgentState(TypedDict):
    user: str
    city: str
    date: str
    duration: str
    room_type: str
    budget: Optional[str]
    db_params: dict
    combinations: List[dict]
    search_results: List[dict]
    final_ranking: str


# 2️⃣ Node 1: Plan the searches
def plan_searches(state: AgentState) -> dict:
    logger.info("--- [NODE] Planning Searches ---")

    planner = SearchPlanner(state["db_params"])

    combs = planner.generate_combinations(
        city=state["city"],
        date=state["date"],
        duration=state["duration"],
        room_type=state["room_type"]
    )

    logger.info(f"Generated {len(combs)} combinations to search.")

    return {"combinations": combs}


# 3️⃣ Node 2: Execute all searches in Parallel
def execute_searches(state: AgentState) -> dict:
    logger.info("--- [NODE] Executing Playwright Searches ---")

    tool = IRCTCSearchTool(headless=True)
    combs = state.get("combinations", [])

    all_results = []
    
    if not combs:
        logger.warning("No combinations to search.")
        return {"search_results": []}

    # Run searches sequentially to avoid Playwright asyncio thread conflicts on Windows
    for c in combs:
        try:
            res = tool.run_search_sync(
                c["station_name"],
                c["date"],
                c["duration"],
                c["room_type"]
            )
            all_results.extend(res)
        except Exception as e:
            logger.error(f"Search task failed for {c['station_name']}: {e}")

    return {"search_results": all_results}


# 4️⃣ Node 3: Rank results using LLM
def rank_results(state: AgentState) -> dict:
    logger.info("--- [NODE] Ranking Results using AI ---")

    ranker = ResultRanker()

    prefs = {
        "city": state["city"],
        "room_type": state["room_type"],
        "duration": state["duration"],
        "budget": state.get("budget", "Any")
    }

    ranking = ranker.rank_results(
        state.get("search_results", []),
        prefs
    )

    return {"final_ranking": ranking}


# 5️⃣ Build LangGraph Workflow
def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("planner", plan_searches)
    workflow.add_node("searcher", execute_searches)
    workflow.add_node("ranker", rank_results)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "ranker")
    workflow.add_edge("ranker", END)

    return workflow.compile()


# 6️⃣ Main function used by frontend
def run_agent(user, city, date, duration, room_type, budget=None):

    db_params = {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "postgres"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "password")
    }

    initial_state = {
        "user": user,
        "city": city,
        "date": str(date),
        "duration": duration,
        "room_type": room_type,
        "budget": budget,
        "db_params": db_params,
        "combinations": [],
        "search_results": [],
        "final_ranking": ""
    }

    graph = build_graph()

    logger.info(">>> STARTING AGENT WORKFLOW <<<")

    try:
        final_state = graph.invoke(initial_state)
        return final_state.get("final_ranking", "No results generated.")
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        return f"Workflow failed: {e}"


# 7️⃣ Test the system
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    result = run_agent(
        "guest",
        "Varanasi",
        "2024-12-01",
        "12h",
        "AC"
    )

    logger.info("===== FINAL RESULT =====")
    logger.info(result)