from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware as cors_middleware

class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl
    # advanced settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    cors_middleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/analyze_video")

def analyze_video(request: VideoAnalysisRequest):
    from langchain_community.document_loaders.youtube import YoutubeLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
  

    # Doing the analysis
    try:
        youtube_url_str = str(request.youtube_link)  # Convert HttpUrl to string
        
        # Extract the video ID from the shortened URL
        if "youtu.be" in youtube_url_str:
            video_id = youtube_url_str.split("/")[-1].split("?")[0]
        else:
            video_id = youtube_url_str.split("v=")[1].split("&")[0]
        loader = YoutubeLoader(video_id=video_id, add_video_info=True)
        docs = loader.load()
        print(f"On Load: {type(docs)}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        result = text_splitter.split_documents(docs)

        print(f"{type(result)}")
        author = result[0].metadata['author']
        length = result[0].metadata['length']
        title = result[0].metadata['title']
        total_size = len(result)
        return {
        "author": author,
        "length": length,
        "title": title,
        "total_size": total_size,
        "text": result[0].page_content 
        }
    except IndexError:
        print("Error: Unable to extract video ID from the provided YouTube URL.")
        print(f"YouTube URL: {youtube_url_str}")
        return {"error": "Invalid YouTube URL format"}
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}

@app.get("/root")
def health():
    return {"status": "ok"}

