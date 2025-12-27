import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic



def __check_anthropic_api():
    load_dotenv()
    try:
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")
        return anthropic_api_key
    except Exception as e:
        print(f"Error checking ANTHROPIC_API_KEY: {e}")
        return None
    
def llm_instance(model: str , temperature: float , timeout: int) -> ChatAnthropic:
    __check_anthropic_api()
    if __check_anthropic_api() is True:
        print("Anthropic API Key found successfully.")
    return ChatAnthropic(model=model, temperature=temperature, timeout=timeout)