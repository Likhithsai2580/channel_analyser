from groq import Groq
from typing import Dict

class ContentSummarizer:
    def __init__(self, client: Groq):
        self.client = client
        
    async def generate_summary(self, transcript: str, visual_analysis: Dict) -> Dict:
        """Generate a comprehensive summary using Llama 3."""
        try:
            # Construct prompt for the LLM
            prompt = self._construct_summary_prompt(transcript, visual_analysis)
            
            # Generate summary using Llama 3
            completion = await self.client.chat.completions.create(
                model="llama3-70b-8192",  # Using the more capable 70B model
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content analyzer. Provide detailed, structured analysis of YouTube content focusing on educational value, key concepts, and practical insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            return {
                'summary': completion.choices[0].message.content,
                'educational_value': self._extract_educational_value(completion.choices[0].message.content)
            }
            
        except Exception as e:
            print(f"Summary generation error: {str(e)}")
            return {}
            
    def _construct_summary_prompt(self, transcript: str, visual_analysis: Dict) -> str:
        """Construct a prompt for the LLM combining transcript and visual analysis."""
        return f"""
        Analyze the following YouTube video content:
        
        TRANSCRIPT:
        {transcript[:2000]}... # Truncated for length
        
        VISUAL ELEMENTS:
        {visual_analysis}
        
        Please provide:
        1. A concise summary of the main educational content
        2. Key concepts and themes discussed
        3. Practical insights and takeaways
        4. Educational value assessment (1-10)
        5. Target audience recommendation
        """ 