import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_vertexai import VertexAI
from langchain.chains.summarize import load_summarize_chain

# Instantiate the VertexAI class
model = VertexAI(model_name="gemini-pro", project="ai-dev-cqc-q1-2024")
# https://youtu.be/lpWvz0dR3wc?si=KNHIrHabfs_r9MEv

st.header("Video info")
screen = st.empty()

with screen.container():
    st.subheader("Youtube Loader")
    
    with st.form("Load video"):
        url = st.text_input("Video URL")
        submit = st.form_submit_button("Load")

    if submit:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        result = loader.load()
        st.write(f"Found video from {result[0].metadata['author']} that is {result[0].metadata['length']} seconds long")
        
        st.subheader("Summarize")
        st.write("Summarize the video using the langchain SummarizeChain")
        
        chain = load_summarize_chain(
            llm = model,
            chain_type="stuff",
            verbose = False
        )
        
        summary = chain.run(result)
        
        st.write(summary)