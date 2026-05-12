import logging
from models.gemini_llm import GeminiLLM
import json

logger = logging.getLogger(__name__)

class ResultRanker:
    def __init__(self):
        # We initialize our Gemini model we built earlier
        self.llm = GeminiLLM().get_llm()

    def rank_results(self, search_results, original_preferences):
        """
        Uses Gemini to analyze and rank the search results based on price, availability, 
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
        
        logger.info("Invoking Gemini API for intelligent ranking...")
        try:
            # We ask the LLM to do the heavy lifting of reading the JSON and reasoning about the best options
            ranked_output = self.llm.invoke(prompt)
            # Gemini returns an AIMessage, so we need to extract the content
            return ranked_output.content
        except Exception as e:
            logger.error(f"Error connecting to LLM: {e}")
            return f"Error connecting to LLM: {e}"
