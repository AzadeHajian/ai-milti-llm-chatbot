import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

def __check_huggingface_api():
    # Placeholder for any token checks if needed in the future
    load_dotenv()
    try:
        huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not huggingface_api_key:
            raise ValueError("HUGGINGFACEHUB is not set in environment variables.")
        return huggingface_api_key
    except Exception as e:
        raise EnvironmentError("Failed to load HUGGINGFACEHUB from environment variables.") from e
                             
def llm_instance(model: str , temperature: float , timeout: int) -> HuggingFaceEndpoint:
    __check_huggingface_api()
    if __check_huggingface_api() is True:
        print("HuggingFace API Key found successfully.")
    return  HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    provider="auto",  # let Hugging Face choose the best provider for you
)




