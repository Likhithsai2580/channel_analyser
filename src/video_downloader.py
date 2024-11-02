import yt_dlp
import os
from typing import Dict, Optional
import cv2
import numpy as np
from pathlib import Path

class VideoDownloader:
    def __init__(self, download_path: str = "temp_downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    async def download_video(self, url: str) -> Dict[str, str]:
        """Download video and extract frames."""
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': str(self.download_path / '%(id)s.%(ext)s'),
                'quiet': True
            }
            
            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = str(self.download_path / f"{info['id']}.mp4")
                
            # Extract frames
            frames_path = self.download_path / f"{info['id']}_frames"
            frames_path.mkdir(exist_ok=True)
            frame_paths = self._extract_frames(video_path, frames_path)
            
            return {
                'video_path': video_path,
                'frame_paths': frame_paths,
                'thumbnail_url': info.get('thumbnail'),
                'title': info.get('title'),
                'duration': info.get('duration')
            }
            
        except Exception as e:
            raise ValueError(f"Error downloading video: {str(e)}")
            
    def _extract_frames(self, video_path: str, frames_path: Path, 
                       frame_interval: int = 30) -> list[str]:
        """Extract frames from video at specified intervals."""
        frame_paths = []
        cap = cv2.VideoCapture(video_path)
        
        try:
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % frame_interval == 0:
                    frame_path = str(frames_path / f"frame_{frame_count}.jpg")
                    cv2.imwrite(frame_path, frame)
                    frame_paths.append(frame_path)
                    
                frame_count += 1
                
        finally:
            cap.release()
            
        return frame_paths
        
    def cleanup(self, video_id: str):
        """Clean up downloaded files."""
        try:
            video_path = self.download_path / f"{video_id}.mp4"
            frames_path = self.download_path / f"{video_id}_frames"
            
            if video_path.exists():
                video_path.unlink()
            if frames_path.exists():
                for frame in frames_path.glob("*.jpg"):
                    frame.unlink()
                frames_path.rmdir()
                
        except Exception as e:
            print(f"Cleanup error: {str(e)}") 