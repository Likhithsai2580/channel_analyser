from groq import Groq
from typing import List, Dict
import asyncio
from pathlib import Path
import base64

class VisualAnalyzer:
    def __init__(self, client: Groq):
        self.client = client
        self.model = "llama-3.2-90b-vision-preview"  # Using the more capable 90B model
        
    async def analyze_frames(self, frame_paths: List[str]) -> Dict:
        """Analyze video frames using Llama Vision."""
        try:
            # Analyze frames in parallel batches
            batch_size = 4
            results = []
            
            for i in range(0, len(frame_paths), batch_size):
                batch = frame_paths[i:i + batch_size]
                batch_tasks = [self._analyze_single_frame(frame_path) 
                             for frame_path in batch]
                batch_results = await asyncio.gather(*batch_tasks)
                results.extend(batch_results)
            
            # Aggregate and summarize results
            return self._aggregate_analysis(results)
            
        except Exception as e:
            print(f"Frame analysis error: {str(e)}")
            return {}
            
    async def _analyze_single_frame(self, frame_path: str) -> Dict:
        """Analyze a single frame using Llama Vision."""
        try:
            # Read and encode image
            with open(frame_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create vision analysis prompt
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze this frame from an educational video. Focus on identifying educational elements, visual aids, and teaching methods."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": "Describe the educational elements and visual content in this frame."
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return {
                'frame_path': frame_path,
                'analysis': completion.choices[0].message.content
            }
            
        except Exception as e:
            print(f"Single frame analysis error: {str(e)}")
            return {'frame_path': frame_path, 'analysis': ''}
            
    def _aggregate_analysis(self, frame_analyses: List[Dict]) -> Dict:
        """Aggregate analyses from multiple frames."""
        try:
            # Combine frame analyses into a comprehensive summary
            combined_prompt = self._create_aggregation_prompt(frame_analyses)
            
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize the visual analysis of multiple video frames into a cohesive educational content analysis."
                    },
                    {
                        "role": "user",
                        "content": combined_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                'frame_count': len(frame_analyses),
                'summary': completion.choices[0].message.content,
                'frame_details': frame_analyses
            }
            
        except Exception as e:
            print(f"Analysis aggregation error: {str(e)}")
            return {} 