import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class YoutubeProcessor:
    # Retrieve the full transcript as a Document then split
    
    def __init__(self):
        """
        Initializes the DocumentProcessor with any required attributes.
        """
        self.pages = []  # List to keep track of pages from all documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 0
        )
        
    def retrieve_youtube_documents(self, video_url: str, chunk_size: int = 1000):
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        result = loader.load()
        
        result = self.text_splitter.split_documents(result)
        
        print(f"Found video from {result[0].metadata['author']} that is {result[0].metadata['length']} seconds long")
        print(f"type: {type(result[0])}")
        print(f"Doc Size: {len(result)}")
    

if __name__ == "__main__":
    
    st.header("Video info")
    screen = st.empty()

    with screen.container():
        st.subheader("Youtube Loader")
        
        with st.form("Load video"):
            url = st.text_input("Video URL")
            submit = st.form_submit_button("Load")

        if submit:
            processor = YoutubeProcessor()
            processor.retrieve_youtube_documents(url)
