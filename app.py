import streamlit as st 
from dotenv import load_dotenv
from mychat.schema import ChatRole, UserMessage, AssistantMessage
from mychat.chatter import CHATTER

load_dotenv(".env", override=True)

def get_avatar(role: ChatRole) -> str:
    
    match role:
        case ChatRole.User:
            return "😎"
        case ChatRole.Assistant:
            return "🤖"

# app title
st.title("My Chatbot 🤖")

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
    history_messages.append(UserMessage(content=query).to_dict())
    
    # get response from the chatter
    response = CHATTER(query)
    
    # print AI's response
    with st.chat_message(name=str(ChatRole.Assistant), avatar=get_avatar(ChatRole.Assistant)):
        st.markdown(response)
        
    # add query to history message
    history_messages.append(AssistantMessage(content=response).to_dict())
    
