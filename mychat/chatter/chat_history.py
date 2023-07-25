from typing import Optional
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, 
    Distance, 
    PointStruct
)

from ..schema import (
    ChatMessage,
    SystemMessage,
    UserMessage
)
from .utils import (
    convert_message_to_str,
    convert_messages_to_str
)
from ..openai_utils import openai_chat, openai_encode_text
from .config import ChatConfig

CHAT_HISTORY_SUMMARY_COLLECTION_NAME = "chat-history-summaries"
EMBEDDING_DIM = 1536

class ChatHistoryManager(QdrantClient):
    
    def __init__(
            self,
            host: str = "localhost", 
            port: int = 6333,
            min_n_messages: int = 8,
            n_messages_to_summarize: int = 4,
            max_n_relevant_summaries: int = 5,
            chat_config: ChatConfig = ChatConfig()
        ):
        
        super().__init__(
            host=host,
            port=port
        )
        
        self._collection_name = CHAT_HISTORY_SUMMARY_COLLECTION_NAME
        
        self.recreate_collection(
            collection_name=self._collection_name,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )
        
        self._collection = self.get_collection(self._collection_name)
        
        self._min_n_messages = min_n_messages
        self._n_messages_to_summarize = n_messages_to_summarize
        self._message_buffer: list[ChatMessage] = []
        self._max_n_relevant_summaries = max_n_relevant_summaries
        self._chat_config = chat_config
    
    @property
    def collections(self) -> list[str]:
        
        return list(map(
            lambda collection: collection.name,
            self.get_collections().collections
        ))
    
    @property
    def chat_history_messages(self) -> list[ChatMessage]:
        
        return self._message_buffer
    
    def insert_message(self, message: ChatMessage):
        
        if len(self._message_buffer) >= self._min_n_messages + self._n_messages_to_summarize:
            
            messages_to_summarize = self._message_buffer[:self._n_messages_to_summarize]
            self._message_buffer = self._message_buffer[self._n_messages_to_summarize:]
            
            summary = self.summarize_chat_history(messages_to_summarize)
            self.insert_summary(summary)
            
        self._message_buffer.append(message)
    
    def insert_summary(self, summary: str):
        
        self.upsert(
            collection_name=self._collection_name,
            points=[
                PointStruct(
                    id=uuid.uuid1().hex,
                    payload={
                        "summary": summary
                    },
                    vector=openai_encode_text(summary)
                )
            ]
        )
    
    def summarize_chat_history(
            self,
            messages: list[ChatMessage]
        ) -> str:
        
        chat_history = convert_messages_to_str(messages)
        
        prompt = (
            "{profile}"
            "The following are your chat history with me: "
            "{chat_history}"
            "Summarize the above chat history by "
            "extracting the key information. "
            "Your summary is:"
        ).format(
            profile=convert_message_to_str(
                SystemMessage(self._chat_config.assistant_profile)
            ),
            chat_history=chat_history
        )
        
        response = openai_chat(
            messages=[
                UserMessage(prompt)
            ]
        )
        
        return response

    def retrieve_relevant_summaries(
            self, 
            query: str,
            max_n_relevant_summaries: Optional[int] = None
        ) -> list[str]:
        
        query_embedding = openai_encode_text(query)
        
        if max_n_relevant_summaries is None:
            max_n_relevant_summaries = self._max_n_relevant_summaries
        
        points = self.search(
            collection_name=self._collection_name,
            query_vector=query_embedding,
            with_payload=True,
            limit=max_n_relevant_summaries
        )
        
        summaries = list(map(
            lambda point: point.payload["summary"],
            points
        ))
        
        return summaries
    