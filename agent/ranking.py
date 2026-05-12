import logging
from models.ollama_llm import Localllm
import json

logger = logging.getLogger(__name__)

class ResultRanker:
    def __init__(self):
        # We initialize our Llama 3 model we built earlier
        self.llm = Localllm().get_llm()

    def rank_results(self, search_results, original_preferences):
        """
        Uses Llama 3 to analyze and rank the search results based on price, availability, 
        and user preferences.
        """
        # First, we filter out any errors or waitlisted rooms. We only want Available rooms!
        valid_results = [res for res in search_results if res.get("availability") == "Available"]
        
        if not valid_results:
            logger.warning("No valid results to rank.")
            return "No available rooms found for your preferences."

        prompt = f"""
        You are an AI travel assistant. Rank the following IRCTC retiring room options from best to worst.
        User Preferences: {json.dumps(original_preferences)}
        
        Options:
        {json.dumps(valid_results, indent=2)}

        Rank them based on:
        1. Lowest price
        2. Matches preferred room type
        
        Return exactly the Top 3 best options in a clear, formatted numbered list. 
        Include the station, room type, price, and duration.
        Do not include any other conversational text.
        """
        
        logger.info("Invoking Llama 3 for intelligent ranking...")
        try:
            # We ask the LLM to do the heavy lifting of reading the JSON and reasoning about the best options
            ranked_output = self.llm.invoke(prompt)
            return ranked_output
        except Exception as e:
            logger.error(f"Error connecting to LLM: {e}")
            return f"Error connecting to LLM: {e}"
