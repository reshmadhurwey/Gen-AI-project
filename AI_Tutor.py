import streamlit as st
import google.generativeai as genai

st.title("🤖 AI Data Science Tutor")

# Step - 1
# Import Chat model and configure the API key
from langchain_google_genai import ChatGoogleGenerativeAI
f = open("C:\\Users\\HP\\Desktop\\Batch 233\\intern 2025\\keys\\gemini.txt")     
key = f.read()
chat_model = ChatGoogleGenerativeAI(model = "gemini-1.5-pro", google_api_key = key)


# Step - 2
# Create Chat Template
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,HumanMessagePromptTemplate


chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="""
        You are known to be a polite and helpful AI assistant who is an expert in Data Science, 
        capable of solving any issue related to data science and providing an exact code example for the user's input. 
        Assist with teaching a Data Science course.You are a chatbot having a conversation with a human. 
        Your role is to assist students in clarifying their doubts regarding specific data science topic.
        If someone asks non-data science related queries, politely tell them to ask relevant questions.
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}")
])


# Step = 3
# Create a Output Parser
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()
   
# Step = 4
# Initialize the Memory
from langchain_core.runnables import RunnableLambda

memory_buffer = {"history":[]}

def get_history_from_buffer(human_input):
    return memory_buffer["history"]

runnable_get_history_from_buffer = RunnableLambda(get_history_from_buffer)
chat_history = runnable_get_history_from_buffer

# Step = 5
# build a chain

from langchain_core.runnables import RunnablePassthrough
chain = RunnablePassthrough.assign(
        chat_history = runnable_get_history_from_buffer
        ) | chat_template | chat_model | output_parser

# Step = 6 
# Invoke the chain with human_input and chat_history
from langchain_core.messages import HumanMessage,AIMessage

# step = 7
# Saving to memory
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    

user_input = st.chat_input("Type your message:")
with st.chat_message("assistant"):
        st.write("Hi.... I am Data Science Tutor. Ask me anything related to Data Science.")

if user_input:
    query= {"human_input" : user_input}
    response = chain.invoke(query)

    memory_buffer["history"].append(HumanMessage(content=query["human_input"]))
    memory_buffer["history"].append(AIMessage(content=response))
    
    st.session_state["chat_history"].append((user_input, response))
    
    if user_input.lower() in ['bye', 'quit', 'exit']:
        st.stop()

st.subheader("Chat History")

for human, ai in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.write(human)
    with st.chat_message("assistant"):
        st.write(ai)

