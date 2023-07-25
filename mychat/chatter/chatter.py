from ..schema import (
    SystemMessage,
    UserMessage,
    AssistantMessage
)
from ..openai_utils import openai_chat
from .utils import (
    convert_message_to_str,
    convert_messages_to_str
)
from .chat_history import ChatHistoryManager
from .config import ChatConfig

class Chatter:
    
    def __init__(
            self,
            chat_history_manager: ChatHistoryManager,
            chat_config: ChatConfig = ChatConfig()
        ) -> None:
        
        self._chat_history_manager = chat_history_manager
        self._chat_config = chat_config
        
        # Sync the chat configuration of the chat history manager
        self._chat_history_manager._chat_config = self._chat_config
        
    def __call__(self, query: str):
        
        self._chat_history_manager.insert_message(
            UserMessage(query)
        )
        
        chat_history = convert_messages_to_str(
            self._chat_history_manager.chat_history_messages
        )
        
        prompt = (
            "Your recent chat history with me is:"
            "{chat_history}"
            "The following summarries of previous conversations may also help:"
            "{chat_history_summary} "
            "Based on the provided information of this ongoing chat, "
            "your response is:"
        ).format(
            chat_history=chat_history,
            chat_history_summary=convert_message_to_str(
                UserMessage(
                    self._chat_history_manager.retrieve_relevant_summaries(query)
                )
            ),
            query=query
        )
        
        response = openai_chat(
            messages=[
                SystemMessage(self._chat_config.assistant_profile),
                UserMessage(prompt)
            ]
        )
        
        self._chat_history_manager.insert_message(
            AssistantMessage(response)
        )
        
        return response
    
    @property
    def assistant_profile(self) -> str:
        return self._chat_config.assistant_profile
    
    @assistant_profile.setter
    def assistant_profile(self, new_profile: str) -> None:
        
        # Update new profile
        self._chat_config._assistant_profile = new_profile
        
        # Also need to update the chat config
        # of the history manager
        self._chat_history_manager._chat_config = self._chat_config
