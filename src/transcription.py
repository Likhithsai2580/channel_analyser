from groq import Groq
import tempfile
from typing import BinaryIO

class AudioTranscriber:
    def __init__(self, client: Groq):
        self.client = client
        
    async def transcribe(self, audio_file: BinaryIO) -> str:
        """Transcribe audio using Groq's Whisper integration."""
        try:
            # Create transcription using Groq's Whisper endpoint
            transcription = await self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="text",
                language="en"  # Can be adjusted based on video language
            )
            return transcription.text
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return "" 