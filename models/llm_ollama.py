from langchain_ollama import ChatOllama


def llm_instance(model: str , temperature: float , timeout: int) -> ChatOllama:
    return ChatOllama(model=model, temperature=temperature, timeout=timeout)





