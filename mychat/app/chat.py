import streamlit as st
from ..schema import (
    ChatRole, 
    UserMessage, 
    AssistantMessage
)
from ..chatter import (
    Chatter,
    ChatHistoryManager,
    ChatConfig
)
from ..chatter.config import (
    DEFAULT_USER_NAME,
    DEFAULT_ASSISTANT_NAME,
    DEFAULT_ASSISTANT_PROFILE
)

def get_avatar(role: ChatRole) -> str:
    
    match role:
        case ChatRole.User:
            return "😎"
        case ChatRole.Assistant:
            return "🤖"

def chat():
    
    print("Enter chat room")

    # app title
    st.title("My Chatbot 🤖")

    # get chatter
    if "chatter" not in st.session_state:
        
        print("Create a new chatter")
        
        st.session_state.user_name = "Isaac"
        st.session_state.assistant_name = "Natia"
        
        st.session_state.chatter = Chatter(
            chat_history_manager=ChatHistoryManager(
                host="localhost",
                port=6333,
                min_n_messages=8,
                n_messages_to_summarize=4,
                max_n_relevant_summaries=5
            ),
            chat_config=ChatConfig(
                user_name=st.session_state.get("user_name", DEFAULT_USER_NAME),
                assistant_name=st.session_state.get("assistant_name", DEFAULT_ASSISTANT_NAME),
                assistant_profile=st.session_state.get("assistant_profile", DEFAULT_ASSISTANT_PROFILE)
            )
        )
    chatter = st.session_state.chatter

    # load history messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    history_messages = st.session_state.messages

    # print history
    for message in history_messages:
        role_name = message["role"]
        content = message["content"]
        role = ChatRole.from_str(role_name)
        with st.chat_message(name=role_name, avatar=get_avatar(role)):
            st.markdown(content)

    # get user's query   
    query = st.chat_input("I want to ask...")

    if query is not None:
        
        # print user's query
        with st.chat_message(name=str(ChatRole.User), avatar=get_avatar(ChatRole.User)):
            st.markdown(query)
            
        # add query to history message
        history_messages.append(UserMessage(query).to_dict())
        
        # get response from the chatter
        response = chatter(query)
        
        # print AI's response
        with st.chat_message(name=str(ChatRole.Assistant), avatar=get_avatar(ChatRole.Assistant)):
            st.markdown(response)
            
        # add query to history message
        history_messages.append(AssistantMessage(content=response).to_dict())
