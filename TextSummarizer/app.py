import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

#streamlit app
st.set_page_config(page_title="Summarize Text from Youtube or Website",page_icon="📚")
st.title("Summarize Text from Youtube or Website")
st.subheader("Summarize URL")

#Get the grop API key and url

with st.sidebar:
    groq_api_key = st.text_input("Enter your GROQ API Key",value="", type="password")

generic_url = st.text_input("Enter the URL", label_visibility="collapsed")

llm = ChatGroq(model="Gemma-7b-It",groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""

prompt = PromptTemplate(template= prompt_template, input_variables=["text"])
if st.button("Summarize the content from Youtube or Website"):
    #vaildate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Provide provide the informatino")
    elif not validators.url(generic_url):
        st.error("Please provide a valid URL. Can be a youtube video url or website url")
    else:
        try:
            with st.spinner("Waiting..."):
                ##loading the website of youtube data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info= True)
                else:
                    loader= UnstructuredURLLoader(urls=[generic_url],ssl_verify=False)
                docs = loader.load()

                ##Chain for summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")