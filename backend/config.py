"""
CareerForge AI - Configuration Module
Environment-based configuration with sensible defaults.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    """LLM Service Configuration"""
    # Ollama API endpoint (local or remote)
    base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    
    # Primary model for career guidance
    model: str = os.getenv("LLM_MODEL", "mistral:7b-instruct-v0.3-q4_K_M")
    
    # Fallback model if primary unavailable
    fallback_model: str = os.getenv("LLM_FALLBACK_MODEL", "mistral:7b-instruct")
    
    # Request timeout in seconds
    timeout: int = int(os.getenv("LLM_TIMEOUT", "120"))
    
    # Max retries on failure
    max_retries: int = int(os.getenv("LLM_MAX_RETRIES", "3"))
    
    # Temperature (0-1, lower = more deterministic)
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    # Max tokens for response
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "4096"))


@dataclass
class APIConfig:
    """API Server Configuration"""
    # Server host
    host: str = os.getenv("API_HOST", "0.0.0.0")
    
    # Server port
    port: int = int(os.getenv("API_PORT", "8000"))
    
    # Debug mode
    debug: bool = os.getenv("API_DEBUG", "false").lower() == "true"
    
    # CORS allowed origins (comma-separated)
    cors_origins: list = None
    
    # Rate limiting (requests per minute)
    rate_limit: int = int(os.getenv("RATE_LIMIT", "30"))
    
    def __post_init__(self):
        origins = os.getenv("CORS_ORIGINS", "*")
        self.cors_origins = [o.strip() for o in origins.split(",")]


@dataclass
class YouTubeConfig:
    """YouTube Scraping Configuration"""
    # Whether to fetch YouTube videos
    enabled: bool = os.getenv("YOUTUBE_ENABLED", "true").lower() == "true"
    
    # Max videos per search
    max_videos: int = int(os.getenv("YOUTUBE_MAX_VIDEOS", "3"))
    
    # Minimum video duration in seconds (filters out shorts)
    min_duration: int = int(os.getenv("YOUTUBE_MIN_DURATION", "600"))


# Singleton instances
llm_config = LLMConfig()
api_config = APIConfig()
youtube_config = YouTubeConfig()


# Logging configuration
def get_log_level() -> str:
    """Get logging level from environment."""
    return os.getenv("LOG_LEVEL", "INFO").upper()


# Print configuration on startup (without secrets)
def print_config():
    """Print current configuration for debugging."""
    print("=" * 60)
    print("CareerForge AI - Configuration")
    print("=" * 60)
    print(f"LLM Base URL:     {llm_config.base_url}")
    print(f"LLM Model:        {llm_config.model}")
    print(f"LLM Fallback:     {llm_config.fallback_model}")
    print(f"LLM Timeout:      {llm_config.timeout}s")
    print(f"API Host:         {api_config.host}")
    print(f"API Port:         {api_config.port}")
    print(f"Debug Mode:       {api_config.debug}")
    print(f"Rate Limit:       {api_config.rate_limit}/min")
    print(f"YouTube Enabled:  {youtube_config.enabled}")
    print("=" * 60)
