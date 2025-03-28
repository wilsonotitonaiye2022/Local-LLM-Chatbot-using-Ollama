# Description: This file contains the code for the Streamlit app that uses the Ollama framework and Langchain to create a chatbot.
# The chatbot is able to answer questions based on the conversation history.

# Import the required libraries
import streamlit as st
from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
import system_prompting

# Define a function to get the response from the chatbot
def get_response(user_query, chat_history, model_selected):
    llm = OllamaLLM(model=model_selected)#"gemma3:12b"
    template = system_prompting.CHAT_SYSTEM_PROMPT
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query
        })

# Set the page configuration
st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖", layout = "wide")
st.title("Local LLM Chatbot using Ollama")

with st.sidebar:
    st.subheader("About")
    st.info("""
            This is a chatbot that answers questions based on the conversation history. 
            The app uses the Ollama framework and Langchain to create a chatbot that can answer 
            questions based on the conversation history. Please type your message in the chat window 
            and the chatbot will respond accordingly. The chatbot uses a local LLM model to generate 
            responses. The chatbot can answer questions based on the conversation history."
            """)
    
    

    model_selected = st.selectbox(
    "**PLEASE SELECT A MODEL:**",
    ("gemma3:12b", "llama3.2", "phi4"), 0)

    st.info("Please refresh the browser to reset the session if you want to use a different model", icon="🚨")

    #Refresh button to clear the session
    if st.button("Refresh"):
        st.session_state.clear()  # Clears all stored session state variables
        st.experimental_rerun()   # Forces a full rerun of the script
st.info("""
           You can select from 3 different models. The default model is **GEMMA 3:12b**.
           The other models are **LLAMA 3.2** and **PHI 4**. The models are locally installed on the Ollama framework.
        """)

st.success(f'You have seleceted the {model_selected} model. To work with a different model, please select from the dropdown in the side bar.')


# Check if the chat history is in the session state
# If not, initialize the chat history with a welcome message
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi, I am an AI Assistant. How can I help you?")]

# Display the chat history
# Loop through the chat history and display the messages
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Get the user query
# If the user query is not empty, add the user query to the chat history
user_query = st.chat_input("Type your message here...")

# Display the user query as a human message
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history, model_selected))

    st.session_state.chat_history.append(AIMessage(content=response))