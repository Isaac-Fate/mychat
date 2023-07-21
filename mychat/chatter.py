from xpyutils import singleton
import json
from .schema import (
    SystemMessage,
    UserMessage,
    AssistantMessage
)
from .utils import call_openai_chat
from .chat_history import ChatHistoryBuffer
from .reflexion import reflect

@singleton
class Chatter:
    
    profile = SystemMessage(
        content=(
            "Your name is Natia from now on "
            "Your goal is to chat with me and help me with my questions."
        )
    )
    
    def __init__(self) -> None:
        
        self._chat_history_buffer = ChatHistoryBuffer()
    
    def __call__(self, query: str) -> str:
        
        self._chat_history_buffer.insert_message(
            UserMessage(content=query)
        )
        
        chat_history = str(self._chat_history_buffer)
        query = str(self._chat_history_buffer.get_last_user_message())
        
        reflection_and_query = json.loads(
            reflect(chat_history)
        )
        
        # unpack reflection and query
        reflection = reflection_and_query["reflection"]
        query = reflection_and_query["query"]
        
        response = call_openai_chat(
            messages=[
                self.profile,
                UserMessage(
                    content=(
                        "The following are chat history messages:\n"
                        "{chat_history}"
                    ).format(
                        chat_history=chat_history
                    )
                ),
                UserMessage(
                    content=(
                        "To better assist the user, you have relfected on your responses. "
                        "Your reflection is: {reflection}"
                    ).format(
                        reflection=reflection
                    )
                ),
                UserMessage(
                    (
                        "My current query is: {query}"
                    ).format(
                        query=query
                    )
                )
            ]
        )
        
        self._chat_history_buffer.insert_message(
            AssistantMessage(content=response)
        )
        
        # print()
        # print(str(self._chat_history_buffer))
        # print()
        
        return response

CHATTER = Chatter()
    