import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

class GeminiLLM:
    def __init__(self, model_name=None, temperature=0.1):
        """Initialize the Gemini model."""
        if model_name is None:
            model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set in the environment variables.")
            
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key
        )

    def get_llm(self):
        return self.llm
        
    def generate_ranking(self, prompt):
        """Helper method to invoke the model directly."""
        return self.llm.invoke(prompt)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    
    llm = GeminiLLM()
    logger.info("Asking Gemini to say hello ...")
    response = llm.generate_ranking("reply with exactly: 'hello from Gemini!'")
    # Langchain Chat models return AIMessage, so we print the content
    logger.info(f"Response: {response.content}")
