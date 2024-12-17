import streamlit as st
from Database.chat_history import ChatHistory
from streamlit_extras.stylable_container import stylable_container
from styling.css import conversation_button
import os
from main import financial_bot
import tempfile
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

st.title("Financial Data Bot (USA)")

# Initialize chat history
if "userid" not in st.session_state:
    st.session_state.userid = 1


################
# Chat History #
################

# Chat History Object
chat_data = ChatHistory(user_id=st.session_state.userid, SUPABASE_API_KEY=SUPABASE_API_KEY)

# Get the list of conversations and sort by conversation_id in descending order
conversation_history = chat_data.get_chat_history(user_id=st.session_state.userid, last_n=5)

# By default no conversation is selected
selected_conversation = None

###########
# Sidebar #
###########

# Sidebar to start a new chat

with st.sidebar:
    with stylable_container(
            key="conversation_button",
            css_styles=conversation_button,
        ): 
        if st.button("New Chat", key="new_chat_button"):
            st.session_state.conversation_id = 0
            st.session_state.messages = []
    

# Sidebar to display recent conversations

st.sidebar.subheader("Recent Conversations")

for conversation in conversation_history:

    button_label = conversation['conversation_name'] or f"Conversation {conversation['conversation_id']}"

    with st.sidebar:

        unique_key = f"conversation_button_{conversation['conversation_id']}"

        with stylable_container(
            key="conversation_button",
            css_styles=conversation_button,
        ): 
            if st.button(button_label, key=unique_key):
                selected_conversation = conversation['conversation_id']

        st.empty()

##################################
# Loading Selected Converstation #
##################################

# Load the selected conversation's messages if a conversation is selected
if selected_conversation:
    conversation_messages = chat_data.get_conversation_history(user_id=st.session_state.userid, conversation_id=selected_conversation)
    st.session_state.conversation_id = selected_conversation    
    st.session_state.messages = conversation_messages

else:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = 0

######################
# Print Chat History #
######################

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)


###########
# Chatbot #
###########

# React to user input
if prompt := st.chat_input("What is up?"):
   
    # User query
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    complete_response = financial_bot(query=prompt, chat_history=st.session_state.messages, gemini_api_key=gemini_api_key)

    with st.chat_message("assistant"):
        message_placeholder = st.empty() 

        message_placeholder.markdown(complete_response, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": complete_response})

    # If new conversation, create new chat history in database
    if st.session_state.conversation_id==0:

        output = chat_data.create_new_messages(user_id=st.session_state.userid, chat_name=prompt, messages=st.session_state.messages)
        st.session_state.conversation_id = output

    # If not a new conversation, update chat history in database
    else:
        chat_data.append_messages(user_id=st.session_state.userid, conversation_id=st.session_state.conversation_id, messages=st.session_state.messages)


