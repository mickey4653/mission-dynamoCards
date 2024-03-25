import streamlit as st
from langchain_community.document_loaders import YoutubeLoader

st.header("Video info")
screen = st.empty()

with screen.container():
    st.subheader("Youtube Loader")
    
    ######################
    #   YOUR CODE HERE   #
    ######################
    
    # Use the langchain YoutubeLoader class to create a loader object.
    # The loader object should be named "loader".
    # The loader should be able to load a video from a given url.
    # The loader should be able to return the duration of the video.
    # The loader should be able to return the type
    # The loader should be able to return the title
    # The loader should be able to return the content