from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware as cors_middleware
from services.genai import (
    YoutubeProcessor, 
    GeminiProcessor)
import logging

# configure log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

genai_processor = GeminiProcessor(
        model_name="gemini-pro",
        project="gemini-dynamo"
    )
@app.post("/analyze_video")

async def analyze_video(request: VideoAnalysisRequest):
    try: 
        # Doing the analysis
        processor = YoutubeProcessor(genai_processor=genai_processor)
        result = processor.retrieve_youtube_documents(str(request.youtube_link), verbose=True)
        logging.info(f"Retrieved documents:", result)  # Debugging statement
        # summary = genai_processor.generate_document_summary(result, verbose=True)
    
        if result:
            # Find key concepts
            logging.info(f"Number of documents: %s", len(result))  # Debugging statement
            key_concepts_list = processor.find_key_concepts(result, verbose=True)
    
            return {
            # "Summary ": summary
            "key_concepts": key_concepts_list
            }
        else:
            raise HTTPException(status_code=404, detail="No documents found")
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    
@app.get("/root")
def health():   
    return {"status": "ok"}

