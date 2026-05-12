import os
import logging
from langchain_community.llms import Ollama  # Note the capital 'O'

logger = logging.getLogger(__name__)

class Localllm:
    def __init__(self, model_name=None, temperature=0.1):
        """Initialize the ollama model."""
        if model_name is None:
            model_name = os.getenv("OLLAMA_MODEL_NAME", "llama3")
        self.llm = Ollama(model=model_name, temperature=temperature)

    def get_llm(self):
        return self.llm
        
    def generate_ranking(self, prompt):
        """Helper method to invoke the model directly."""
        return self.llm.invoke(prompt)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    
    llm = Localllm()
    logger.info("Asking llama 3 to say hello ...")
    response = llm.generate_ranking("reply with exactly: 'hello from llama 3!'")
    logger.info(f"Response: {response}")
