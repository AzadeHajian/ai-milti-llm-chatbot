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
        raise EnvironmentError("Failed to load ANTHROPIC_API_KEY from environment variables.") from e
    
def llm_instance(model: str , temperature: float , timeout: int) -> ChatAnthropic:
    __check_anthropic_api()
    return ChatAnthropic(model=model, temperature=temperature, timeout=timeout)


#if __name__ == "__main__":                                 
## Example usage
#   llm = llm_instance("claude-3-5-sonnet-20241022", temperature=0.7, timeout=60)
#response = llm.invoke("Hello, how are you?")
#print(response.content)
# 
  
    
    