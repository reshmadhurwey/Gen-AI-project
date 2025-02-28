import streamlit as st
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate


st.title('✈️ AI Travel Planner')
source = st.text_input("📍Source")
destination = st.text_input("📌Destination")

date = st.date_input("📆 Select a Date", value= None, min_value= "today")
st.write("Selected date:", date)


# logic 1
chat_template = ChatPromptTemplate(
    messages=[("system","""You are a helpful AI assistance who gives approximated cost of travel from source to destination. 
                Provide a structured response containing different travel modes(bus, car, flight, train ,taxi) and their estimated prices shown in table form.
                Provide the response with travel recommendations."""),
              ("human","Book a transport from {source} to {destination} on {date}")],
)

# logic 2
from langchain_google_genai import ChatGoogleGenerativeAI
f = open("C:\\Users\\HP\\Desktop\\Batch 233\\intern 2025\\keys\\gemini.txt")     
key = f.read()
chat_model = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-exp", google_api_key = key)


# logic 3 
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()


chain = chat_template | chat_model | parser
raw_input = {"source": source ,"destination": destination, "date":date }
response = chain.invoke(raw_input)


if (st.button("Search")):
    st.markdown(response)