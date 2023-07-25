import openai
import os
from .schema import ChatMessage

MODEL_NAME = "gpt-3.5-turbo-16k"

def openai_chat(
        messages: list[ChatMessage],
        *,
        model_name: str = MODEL_NAME,
        temperature: float = 0.0,
        **kwargs
    ) -> str:
    
    # set API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # get response from GPT
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=list(map(
            lambda message: message.to_dict(),
            messages
        )),
        temperature=temperature,
        **kwargs
    ).choices[0].message.content
    
    return response

def openai_encode_text(text: str) -> list[float]:
    
    # set API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    
    embedding = response["data"][0]["embedding"]
    
    return embedding
