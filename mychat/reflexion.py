import json
from .schema import (
    SystemMessage,
    UserMessage
)
from .utils import call_openai_chat

out = {
    "reflection": "",
    "query": ""
}

output_format = json.dumps(out)

PROMPT_TEMPLATE = (
    "The following is your chat history with the user:\n{chat_history}\n"
    "Figure out currently what does the user want to know the most. "
    "(Let's call it 'query')"
    "Reflecting on the chat history, "
    "think about how you can better reply to user's current query. "
    'Your output should be in JSON format: {output_format} '
    'where "reflection" is your reflection and '
    '"query" is the thing that the user currently want to know the most. '
    "Your JSON output is:"
)

def reflect(chat_history: str) -> str:
    
    prompt = PROMPT_TEMPLATE.format(
        chat_history=chat_history,
        output_format=output_format
    )
    
    response = call_openai_chat(
        messages=[
            SystemMessage("You are a helpful assistant to the user by anwsering the question."),
            UserMessage(prompt)
        ]
    )
    
    return response
    