import os
from dotenv import load_dotenv

from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

# for langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT") 

##Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful asistant. Please respond to the question asked"),
        ("user","Question :{question}"),
    ]
)

#streamlit framework
st.title("Langchain Demo With Gemma2")
input_text = st.text_input("What is your question?")

## Ollama gemma2 model
llm = Ollama(model = "gemma2:2b")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question" : input_text}))
