import google.generativeai as genai
import streamlit as st 

f = open("C:\\Users\\HP\\Desktop\\Batch 233\\intern 2025\\keys\\gemini.txt")     
key = f.read()
genai.configure(api_key=key)

system_prompt = """analyze the submitted code and identify potential bugs, errors,
                 or areas of improvement explain it in points and also provide the fixed code snippets."""

model  = genai.GenerativeModel(model_name = 'models/gemini-2.0-flash-exp',
                               system_instruction=system_prompt)



title = st.title('An AI Code Reviewer')

code = st.text_area("Enter your Python code here...",value="",height=300)

response = model.generate_content(code)

if(st.button("Generate")):
    st.subheader("Code Review")
    st.markdown(response.text)



