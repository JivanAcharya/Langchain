from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)


#1. Creat prompt template
generic_template = "Tranlate the following into {language}"
prompt = ChatPromptTemplate.from_messages([
    ("system",generic_template),
    ("user","{text}"),
])

#2. Create output parser
output_parser = StrOutputParser()

#3. Create chain
chain = prompt | model | output_parser

#4. Create FastAPI app
app = FastAPI(title = "Langchain Server",
              version="1.0",
              description="A simple API server using Langserve")

#adding chain routes
add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost",port=8000)