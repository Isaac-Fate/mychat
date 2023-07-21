from typing import Optional
from .schema import ChatRole, ChatMessage
    
class ChatHistoryBuffer:
    
    def __init__(self) -> None:
        
        self._buffer: list[ChatMessage] = []
        
    def __str__(self) -> str:
        
        return "\n".join(map(
            str,
            self._buffer
        ))
    
    @property
    def history_messages(self) -> list[ChatMessage]:
        return self._buffer
    
    def insert_message(self, message: ChatMessage):
        
        self._buffer.append(message)
        
    def get_last_user_message(self) -> Optional[ChatMessage]:
        
        for message in reversed(self._buffer):
            if message.role == ChatRole.User:
                return message
            
        return None
        
if __name__ == "__main__":
    
    buffer = ChatHistoryBuffer()
    buffer.insert_message(
        ChatMessage(
            role=ChatRole.User,
            content="hi"
        )
    )
    buffer.insert_message(
        ChatMessage(
            role=ChatRole.Assistant,
            content="how may I help you?"
        )
    )
    buffer.insert_message(
        ChatMessage(
            role=ChatRole.User,
            content="What is the value of 1 + 1?"
        )
    )
    buffer.insert_message(
        ChatMessage(
            role=ChatRole.Assistant,
            content="It is 2"
        )
    )
    print(str(buffer))
    print(str(buffer.get_last_user_message()))
    