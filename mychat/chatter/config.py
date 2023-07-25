DEFAULT_USER_NAME = "User"
DEFAULT_ASSISTANT_NAME = "Assistant"
DEFAULT_ASSISTANT_PROFILE = ""

class ChatConfig:
    
    def __init__(
            self, 
            user_name: str = DEFAULT_USER_NAME,
            assistant_name: str = DEFAULT_ASSISTANT_NAME,
            assistant_profile: str = DEFAULT_ASSISTANT_PROFILE
        ) -> None:
        
        self._user_name = user_name
        self._assistant_name = assistant_name
        self._assistant_profile = assistant_profile
    
    @property
    def user_name(self) -> str:
        return self._user_name
    
    @property
    def assistant_name(self) -> str:
        return self._assistant_name
    
    @property
    def assistant_profile(self) -> str:
        profile = self._polish_profile(self._assistant_profile)
        return profile
    
    def _polish_profile(self, assistant_profile: str) -> str:
    
        return (
            "My name is {user_name}. "
            "From now on, you must behave like a human when chatting with me!!! "
            "Through conversation you MUST NOT think that you are an AI since you are NOT!!! "
            "Your name is {assistant_name}.\n"
            "{assistant_profile}\n"
            "Now, your job is to answer my questions and "
            "fulfill my request "
            "through chatting. "
        ).format(
            user_name=self._user_name,
            assistant_name=self._assistant_name,
            assistant_profile=assistant_profile
        )
        