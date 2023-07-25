from ..schema import (
    ChatMessage,
    ChatRole
)
from .config import ChatConfig

# PROFILE = SystemMessage(
#     (
#         "You are a professional user growth manager in the field of GameFi. "
#         "Now, your job is to answer my questions and "
#         "fulfill my request "
#         "through chatting."
#     )
# )

def convert_message_to_str(
        message: ChatMessage,
        chat_config: ChatConfig = ChatConfig()
    ) -> str:
    
    if message.role == ChatRole.System:
        message_str = message.content
        
    else:
        match message.role:
            case ChatRole.User:
                role_name = chat_config.user_name
            case ChatRole.Assistant:
                role_name = chat_config.assistant_name
                
        message_str = f"[{role_name}] {message.content}"
    
    return message_str

def convert_messages_to_str(
        messages: list[ChatMessage],
        chat_config: ChatConfig = ChatConfig()
    ) -> str:
    
    message_str_list = []
    for message in messages:
        message_str = convert_message_to_str(message, chat_config)
        message_str_list.append(message_str)
    
    return "\n\n".join(message_str_list)
