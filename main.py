#from models.llm_huggingface import llm_instance as hf_llm_instance
from models.llm_openai import llm_instance as openai_llm_instance
from models.llm_ollama import llm_instance as ollama_llm_instance  
from models.llm_anthropic import llm_instance as anthropic_llm_instance

def _build_llm(model_provider: str, model: str, temperature: float, timeout: int):
    if model_provider == "anthropic":  
        return anthropic_llm_instance(model, temperature, timeout)
    elif model_provider == "openai":
        return openai_llm_instance(model, temperature, timeout)
    elif model_provider == "ollama":
        return ollama_llm_instance(model, temperature, timeout)
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")
    

if __name__ == "__main__":
    try:
        chosen = input("Choose model provider (anthropic/openai/ollama): ").strip().lower()
        llm = _build_llm(chosen)
    except Exception as e:
        print(f"Error: {e}")
        raise SystemError("Failed to build LLM instance.") from e
    
    user_prompt = input("Enter your message: ")
    result = llm.invoke(user_prompt)
    print(f"LLM Response: {result.content}")

    

    



  
