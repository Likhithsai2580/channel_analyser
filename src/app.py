from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_analyzer import YouTubeAnalyzer

app = FastAPI()
analyzer = YouTubeAnalyzer()

class VideoRequest(BaseModel):
    url: str

@app.post("/analyze")
async def analyze_video(request: VideoRequest):
    """Endpoint to analyze a YouTube video."""
    try:
        analysis = await analyzer.analyze_video(request.url)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 