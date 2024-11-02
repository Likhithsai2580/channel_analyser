import os
from groq import Groq
from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timedelta
import aiohttp
from .video_downloader import VideoDownloader
from .visual_analyzer import VisualAnalyzer
from .transcription import AudioTranscriber
from .summarizer import ContentSummarizer

class RateLimiter:
    def __init__(self, calls_per_minute: int = 10):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        
    async def acquire(self):
        """Acquire permission to make an API call."""
        now = datetime.now()
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < timedelta(minutes=1)]
        
        if len(self.calls) >= self.calls_per_minute:
            wait_time = 60 - (now - self.calls[0]).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                
        self.calls.append(now)

class YouTubeAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the YouTube Analyzer with Groq API key."""
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required")
            
        self.client = Groq(api_key=self.api_key)
        self.downloader = VideoDownloader()
        self.visual_analyzer = VisualAnalyzer(self.client)
        self.transcriber = AudioTranscriber(self.client)
        self.summarizer = ContentSummarizer(self.client)
        self.rate_limiter = RateLimiter()
        
    async def analyze_video(self, video_url: str) -> Dict:
        """Analyze a single YouTube video."""
        try:
            # Download video and extract components
            video_data = await self.downloader.download_video(video_url)
            
            # Run analysis tasks concurrently
            await self.rate_limiter.acquire()
            analysis_tasks = [
                self._transcribe_audio(video_data['video_path']),
                self.visual_analyzer.analyze_frames(video_data['frame_paths'])
            ]
            
            transcript, visual_analysis = await asyncio.gather(*analysis_tasks)
            
            # Generate final summary
            await self.rate_limiter.acquire()
            summary = await self.summarizer.generate_summary(transcript, visual_analysis)
            
            return {
                'url': video_url,
                'title': video_data['title'],
                'duration': video_data['duration'],
                'transcript': transcript,
                'visual_analysis': visual_analysis,
                'summary': summary
            }
            
        except Exception as e:
            raise ValueError(f"Video analysis failed: {str(e)}")
            
        finally:
            # Cleanup downloaded files
            if 'video_data' in locals():
                video_id = video_data['video_path'].stem
                self.downloader.cleanup(video_id)