from abc import ABC, abstractmethod
from datetime import datetime

class BaseMemory:
    
    @property
    def timestamp(self) -> datetime:
        """Creation time of the memory.
        """
        return getattr(self, "_timestamp")
    
    @property
    def role(self) -> str:
        """Owner of the memory.
        """
        return getattr(self, "_role")
    
    @property
    def content(self) -> str:
        """Memory content.
        """
        return getattr(self, "_content")
    
    