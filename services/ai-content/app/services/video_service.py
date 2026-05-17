"""
Video Service for video assembly and processing
"""

import subprocess
import os
import logging
from typing import List, Dict, Any
import asyncio
import httpx
from ..core.config import settings

logger = logging.getLogger(__name__)

class VideoService:
    """Service for video assembly and processing"""
    
    def __init__(self):
        self.pexels_api_key = settings.PEXELS_API_KEY
        self.pexels_base_url = "https://api.pexels.com/v1"
    
    async def assemble_video(
        self,
        script: str,
        voice_url: str,
        format: str,
        platforms: List[str],
        background_music: str = None
    ) -> str:
        """
        Assemble video using FFmpeg with voice, visuals, and music
        """
        try:
            logger.info(f"Starting video assembly for format: {format}, platforms: {platforms}")
            
            # Step 1: Get stock footage based on script
            stock_footage = await self._get_stock_footage(script)
            
            # Step 2: Create video composition
            video_url = await self._create_video_composition(
                voice_url=voice_url,
                stock_footage=stock_footage,
                format=format,
                platforms=platforms,
                background_music=background_music
            )
            
            logger.info(f"Video assembly completed: {video_url}")
            return video_url
            
        except Exception as e:
            logger.error(f"Error assembling video: {str(e)}")
            raise Exception(f"Failed to assemble video: {str(e)}")
    
    async def _get_stock_footage(self, script: str) -> List[Dict[str, str]]:
        """
        Get relevant stock footage from Pexels API
        """
        try:
            # Extract keywords from script for video search
            keywords = self._extract_keywords(script)
            
            footage_urls = []
            for keyword in keywords[:3]:  # Limit to 3 keywords
                footage = await self._search_pexels_videos(keyword)
                if footage:
                    footage_urls.extend(footage)
            
            logger.info(f"Found {len(footage_urls)} stock footage clips")
            return footage_urls
            
        except Exception as e:
            logger.error(f"Error getting stock footage: {str(e)}")
            return []
    
    async def _search_pexels_videos(self, query: str, per_page: int = 5) -> List[Dict[str, str]]:
        """
        Search for videos on Pexels
        """
        try:
            headers = {
                "Authorization": self.pexels_api_key
            }
            
            params = {
                "query": query,
                "per_page": per_page,
                "orientation": "portrait"  # Good for mobile platforms
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.pexels_base_url}/videos/search",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    videos = []
                    
                    for video in data.get("videos", []):
                        # Get the best quality video file
                        video_files = video.get("video_files", [])
                        if video_files:
                            # Sort by quality (prefer HD)
                            video_files.sort(key=lambda x: x.get("width", 0), reverse=True)
                            best_video = video_files[0]
                            
                            videos.append({
                                "url": best_video["link"],
                                "duration": video.get("duration", 0),
                                "width": best_video.get("width", 0),
                                "height": best_video.get("height", 0)
                            })
                    
                    logger.info(f"Found {len(videos)} videos for query: {query}")
                    return videos
                else:
                    logger.error(f"Pexels API error: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching Pexels videos: {str(e)}")
            return []
    
    def _extract_keywords(self, script: str) -> List[str]:
        """
        Extract keywords from script for video search
        """
        # Simple keyword extraction (in production, use NLP libraries)
        words = script.lower().split()
        
        # Filter out common words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "can", "this", "that", "these", "those"
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return top keywords
        return keywords[:5]
    
    async def _create_video_composition(
        self,
        voice_url: str,
        stock_footage: List[Dict[str, str]],
        format: str,
        platforms: List[str],
        background_music: str = None
    ) -> str:
        """
        Create video composition using FFmpeg
        """
        try:
            # Determine video dimensions based on platforms
            dimensions = self._get_platform_dimensions(platforms)
            
            # Create output directory
            output_dir = "generated_videos"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"video_{timestamp}.mp4")
            
            # Build FFmpeg command
            ffmpeg_cmd = self._build_ffmpeg_command(
                voice_url=voice_url,
                stock_footage=stock_footage,
                output_file=output_file,
                dimensions=dimensions,
                background_music=background_music
            )
            
            # Execute FFmpeg command
            result = await self._execute_ffmpeg(ffmpeg_cmd)
            
            if result.returncode == 0:
                logger.info(f"Video created successfully: {output_file}")
                return f"/videos/{os.path.basename(output_file)}"
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                raise Exception(f"FFmpeg failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error creating video composition: {str(e)}")
            raise Exception(f"Failed to create video: {str(e)}")
    
    def _get_platform_dimensions(self, platforms: List[str]) -> Dict[str, int]:
        """
        Get video dimensions optimized for platforms
        """
        # Default to 9:16 (vertical) for mobile platforms
        if any(platform in ["tiktok", "instagram"] for platform in platforms):
            return {"width": 1080, "height": 1920}
        elif "youtube" in platforms:
            return {"width": 1920, "height": 1080}
        else:
            return {"width": 1080, "height": 1920}  # Default vertical
    
    def _build_ffmpeg_command(
        self,
        voice_url: str,
        stock_footage: List[Dict[str, str]],
        output_file: str,
        dimensions: Dict[str, int],
        background_music: str = None
    ) -> List[str]:
        """
        Build FFmpeg command for video composition
        """
        cmd = ["ffmpeg", "-y"]  # -y to overwrite output file
        
        # Input files
        inputs = []
        
        # Add voice audio
        if voice_url:
            inputs.extend(["-i", voice_url])
        
        # Add stock footage
        for footage in stock_footage[:3]:  # Limit to 3 clips
            inputs.extend(["-i", footage["url"]])
        
        # Add background music if provided
        if background_music:
            inputs.extend(["-i", background_music])
        
        cmd.extend(inputs)
        
        # Video filters
        filters = []
        
        # Scale and crop footage
        for i, footage in enumerate(stock_footage[:3]):
            filter_idx = i + 1  # First input is voice
            filters.append(f"[{filter_idx}:v]scale={dimensions['width']}:{dimensions['height']}:force_original_aspect_ratio=decrease,crop={dimensions['width']}:{dimensions['height']}[v{i}]")
        
        # Concatenate video clips
        if len(stock_footage) > 1:
            concat_inputs = "".join([f"[v{i}]" for i in range(len(stock_footage[:3]))])
            filters.append(f"{concat_inputs}concat=n={len(stock_footage[:3])}:v=1:a=0[vout]")
        else:
            filters.append("[v0]copy[vout]")
        
        # Audio mixing
        audio_inputs = []
        if voice_url:
            audio_inputs.append("[0:a]")
        if background_music:
            audio_inputs.append(f"[{len(stock_footage) + 1}:a]")
        
        if len(audio_inputs) > 1:
            filters.append(f"{''.join(audio_inputs)}amix=inputs={len(audio_inputs)}:duration=first[aout]")
        else:
            filters.append("[0:a]copy[aout]")
        
        # Apply filters
        cmd.extend(["-filter_complex", ";".join(filters)])
        
        # Output settings
        cmd.extend([
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "fast",
            "-crf", "23",
            output_file
        ])
        
        return cmd
    
    async def _execute_ffmpeg(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """
        Execute FFmpeg command asynchronously
        """
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return subprocess.CompletedProcess(
                args=cmd,
                returncode=process.returncode,
                stdout=stdout,
                stderr=stderr
            )
            
        except Exception as e:
            logger.error(f"Error executing FFmpeg: {str(e)}")
            raise Exception(f"FFmpeg execution failed: {str(e)}")
    
    async def optimize_for_platform(self, video_url: str, platform: str) -> str:
        """
        Optimize video for specific platform requirements
        """
        try:
            # Platform-specific optimizations
            optimizations = {
                "youtube": {"max_duration": 60, "format": "mp4", "quality": "high"},
                "tiktok": {"max_duration": 60, "format": "mp4", "quality": "medium"},
                "instagram": {"max_duration": 90, "format": "mp4", "quality": "medium"}
            }
            
            config = optimizations.get(platform, optimizations["youtube"])
            
            # Apply optimizations using FFmpeg
            optimized_url = await self._apply_optimizations(video_url, config)
            
            logger.info(f"Optimized video for {platform}: {optimized_url}")
            return optimized_url
            
        except Exception as e:
            logger.error(f"Error optimizing video for platform: {str(e)}")
            raise Exception(f"Failed to optimize video: {str(e)}")
    
    async def _apply_optimizations(self, video_url: str, config: Dict[str, Any]) -> str:
        """
        Apply platform-specific optimizations
        """
        # Implementation for video optimization
        # This would involve FFmpeg commands for trimming, quality adjustment, etc.
        return video_url



