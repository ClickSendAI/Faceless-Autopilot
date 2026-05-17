"""
OpenAI Service for content generation
"""

import openai
import logging
from typing import Dict, Any
import asyncio
from ..core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for OpenAI API interactions"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_script(
        self,
        topic: str,
        niche: str,
        format: str,
        duration: int,
        style: str = None,
        tone: str = None
    ) -> str:
        """
        Generate a script using OpenAI GPT-4
        """
        try:
            # Build the prompt based on requirements
            prompt = self._build_script_prompt(topic, niche, format, duration, style, tone)
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content creator specializing in viral short-form video content. Create engaging, trend-aware scripts that maximize viewer retention and engagement."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            script = response.choices[0].message.content
            logger.info(f"Generated script for topic: {topic}")
            return script
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            raise Exception(f"Failed to generate script: {str(e)}")
    
    async def optimize_script(self, script: str, platform: str) -> str:
        """
        Optimize script for specific platform
        """
        try:
            platform_prompts = {
                "youtube": "Optimize this script for YouTube Shorts with strong hook and clear value proposition",
                "tiktok": "Optimize this script for TikTok with trending elements and viral potential",
                "instagram": "Optimize this script for Instagram Reels with visual storytelling focus"
            }
            
            prompt = f"{platform_prompts.get(platform, 'Optimize this script')}:\n\n{script}"
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a platform-specific content optimization expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.5
            )
            
            optimized_script = response.choices[0].message.content
            logger.info(f"Optimized script for platform: {platform}")
            return optimized_script
            
        except Exception as e:
            logger.error(f"Error optimizing script: {str(e)}")
            raise Exception(f"Failed to optimize script: {str(e)}")
    
    async def generate_trending_topics(self, niche: str, count: int = 5) -> list:
        """
        Generate trending topics for a specific niche
        """
        try:
            prompt = f"Generate {count} trending topics in the {niche} niche that would perform well on social media platforms. Focus on current trends and viral potential."
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a trend analysis expert with deep knowledge of social media algorithms and viral content patterns."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            topics_text = response.choices[0].message.content
            # Parse the response to extract topics
            topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()]
            logger.info(f"Generated {len(topics)} trending topics for niche: {niche}")
            return topics
            
        except Exception as e:
            logger.error(f"Error generating trending topics: {str(e)}")
            raise Exception(f"Failed to generate trending topics: {str(e)}")
    
    def _build_script_prompt(
        self,
        topic: str,
        niche: str,
        format: str,
        duration: int,
        style: str = None,
        tone: str = None
    ) -> str:
        """Build the prompt for script generation"""
        
        format_guidelines = {
            "short": "15-60 seconds, hook in first 3 seconds, single clear message",
            "medium": "1-3 minutes, structured with intro, main content, conclusion",
            "long": "3-10 minutes, detailed explanation with examples and engagement"
        }
        
        prompt = f"""
        Create a {format} video script about "{topic}" in the {niche} niche.
        
        Requirements:
        - Duration: {duration} seconds
        - Format: {format_guidelines.get(format, 'Standard format')}
        - Niche: {niche}
        - Topic: {topic}
        """
        
        if style:
            prompt += f"\n- Style: {style}"
        
        if tone:
            prompt += f"\n- Tone: {tone}"
        
        prompt += """
        
        The script should:
        1. Start with a strong hook (first 3 seconds)
        2. Deliver clear value to the viewer
        3. Include a call-to-action
        4. Be optimized for social media engagement
        5. Use conversational, engaging language
        
        Format the script with clear timing markers and speaker directions.
        """
        
        return prompt



