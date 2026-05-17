"""
ElevenLabs Service for voice synthesis
"""

import httpx
import logging
from typing import Dict, Any
import asyncio
from ..core.config import settings

logger = logging.getLogger(__name__)

class ElevenLabsService:
    """Service for ElevenLabs API interactions"""
    
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
    
    async def generate_voiceover(
        self,
        text: str,
        voice_id: str = "default",
        speed: float = 1.0,
        stability: float = 0.5,
        similarity_boost: float = 0.5
    ) -> str:
        """
        Generate voiceover using ElevenLabs API
        """
        try:
            # Get available voices if default is requested
            if voice_id == "default":
                voice_id = await self._get_default_voice()
            
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=data,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    # Save audio file and return URL
                    audio_url = await self._save_audio_file(response.content, voice_id)
                    logger.info(f"Generated voiceover with voice: {voice_id}")
                    return audio_url
                else:
                    logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                    raise Exception(f"ElevenLabs API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error generating voiceover: {str(e)}")
            raise Exception(f"Failed to generate voiceover: {str(e)}")
    
    async def get_available_voices(self) -> list:
        """
        Get list of available voices
        """
        try:
            url = f"{self.base_url}/voices"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    voices_data = response.json()
                    voices = []
                    for voice in voices_data.get("voices", []):
                        voices.append({
                            "voice_id": voice["voice_id"],
                            "name": voice["name"],
                            "category": voice.get("category", "unknown"),
                            "description": voice.get("description", "")
                        })
                    
                    logger.info(f"Retrieved {len(voices)} available voices")
                    return voices
                else:
                    logger.error(f"Error getting voices: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting available voices: {str(e)}")
            return []
    
    async def _get_default_voice(self) -> str:
        """
        Get the default voice ID
        """
        try:
            voices = await self.get_available_voices()
            if voices:
                # Prefer professional voices
                for voice in voices:
                    if "professional" in voice["name"].lower() or "business" in voice["name"].lower():
                        return voice["voice_id"]
                # Fallback to first voice
                return voices[0]["voice_id"]
            else:
                # Fallback to a known voice ID
                return "21m00Tcm4TlvDq8ikWAM"
                
        except Exception as e:
            logger.error(f"Error getting default voice: {str(e)}")
            return "21m00Tcm4TlvDq8ikWAM"  # Fallback voice
    
    async def _save_audio_file(self, audio_content: bytes, voice_id: str) -> str:
        """
        Save audio file and return URL
        """
        try:
            import os
            from datetime import datetime
            
            # Create audio directory if it doesn't exist
            audio_dir = "generated_audio"
            os.makedirs(audio_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voiceover_{voice_id}_{timestamp}.mp3"
            filepath = os.path.join(audio_dir, filename)
            
            # Save file
            with open(filepath, "wb") as f:
                f.write(audio_content)
            
            # Return file URL (in production, this would be uploaded to S3)
            return f"/audio/{filename}"
            
        except Exception as e:
            logger.error(f"Error saving audio file: {str(e)}")
            raise Exception(f"Failed to save audio file: {str(e)}")
    
    async def get_voice_characteristics(self, voice_id: str) -> Dict[str, Any]:
        """
        Get characteristics of a specific voice
        """
        try:
            voices = await self.get_available_voices()
            for voice in voices:
                if voice["voice_id"] == voice_id:
                    return voice
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting voice characteristics: {str(e)}")
            return {}



