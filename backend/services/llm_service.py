"""
CareerForge AI - LLM Service
Abstraction layer for interacting with open-source LLMs via Ollama.
Designed for easy model swapping and robust error handling.
"""

import json
import time
import httpx
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import llm_config


@dataclass
class LLMResponse:
    """Structured response from LLM."""
    success: bool
    content: str
    parsed_json: Optional[Dict[str, Any]] = None
    model: str = ""
    latency_ms: int = 0
    tokens_used: int = 0
    error: Optional[str] = None


class LLMService:
    """
    Service for interacting with self-hosted LLMs.
    
    Supports:
    - Ollama (default)
    - vLLM (OpenAI-compatible endpoint)
    - llama.cpp server
    
    All backends expose OpenAI-compatible APIs.
    """
    
    def __init__(
        self,
        base_url: str = None,
        model: str = None,
        fallback_model: str = None,
        timeout: int = None
    ):
        """
        Initialize LLM Service.
        
        Args:
            base_url: Ollama API endpoint (default: from config)
            model: Primary model to use (default: from config)
            fallback_model: Fallback if primary unavailable
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or llm_config.base_url
        self.model = model or llm_config.model
        self.fallback_model = fallback_model or llm_config.fallback_model
        self.timeout = timeout or llm_config.timeout
        self.temperature = llm_config.temperature
        self.max_tokens = llm_config.max_tokens
        
        # HTTP client with connection pooling
        self.client = httpx.Client(timeout=self.timeout)
        
        print(f"[LLM Service] Initialized with model: {self.model}")
        print(f"[LLM Service] Base URL: {self.base_url}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        expect_json: bool = True
    ) -> LLMResponse:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Override temperature
            max_tokens: Override max tokens
            expect_json: Whether to parse response as JSON
        
        Returns:
            LLMResponse with content and metadata
        """
        # Try primary model first
        response = self._call_model(
            model=self.model,
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            expect_json=expect_json
        )
        
        # If primary fails, try fallback
        if not response.success and self.fallback_model:
            print(f"[LLM Service] Primary model failed, trying fallback: {self.fallback_model}")
            response = self._call_model(
                model=self.fallback_model,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                expect_json=expect_json
            )
        
        return response
    
    def _call_model(
        self,
        model: str,
        prompt: str,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
        expect_json: bool
    ) -> LLMResponse:
        """
        Make the actual API call to Ollama.
        
        Uses Ollama's /api/generate endpoint.
        """
        start_time = time.time()
        
        try:
            # Build the request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            # Add system prompt if provided
            if system_prompt:
                payload["system"] = system_prompt
            
            # Request JSON format if expected
            if expect_json:
                payload["format"] = "json"
            
            # Make the request
            response = self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                return LLMResponse(
                    success=False,
                    content="",
                    error=f"API error: {response.status_code} - {response.text}",
                    model=model,
                    latency_ms=latency_ms
                )
            
            # Parse response
            result = response.json()
            content = result.get("response", "").strip()
            tokens_used = result.get("eval_count", 0)
            
            # Try to parse as JSON if expected
            parsed_json = None
            if expect_json:
                parsed_json = self._extract_json(content)
                if parsed_json is None:
                    return LLMResponse(
                        success=False,
                        content=content,
                        error="Failed to parse JSON from response",
                        model=model,
                        latency_ms=latency_ms,
                        tokens_used=tokens_used
                    )
            
            return LLMResponse(
                success=True,
                content=content,
                parsed_json=parsed_json,
                model=model,
                latency_ms=latency_ms,
                tokens_used=tokens_used
            )
            
        except httpx.ConnectError:
            return LLMResponse(
                success=False,
                content="",
                error=f"Cannot connect to LLM service at {self.base_url}. Is Ollama running?",
                model=model,
                latency_ms=int((time.time() - start_time) * 1000)
            )
        except httpx.TimeoutException:
            return LLMResponse(
                success=False,
                content="",
                error=f"LLM request timed out after {self.timeout}s",
                model=model,
                latency_ms=int((time.time() - start_time) * 1000)
            )
        except Exception as e:
            return LLMResponse(
                success=False,
                content="",
                error=f"LLM error: {str(e)}",
                model=model,
                latency_ms=int((time.time() - start_time) * 1000)
            )
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract and parse JSON from LLM response.
        Handles common issues like markdown code blocks.
        """
        # Try direct parsing first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Remove markdown code blocks
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        try:
            return json.loads(cleaned.strip())
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        try:
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(cleaned[start:end])
        except json.JSONDecodeError:
            pass
        
        return None
    
    def check_health(self) -> Tuple[bool, str]:
        """
        Check if the LLM service is healthy.
        
        Returns:
            Tuple of (is_healthy, status_message)
        """
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                
                if any(self.model in name for name in model_names):
                    return True, f"Healthy - Model {self.model} available"
                elif model_names:
                    return True, f"Healthy - Available models: {', '.join(model_names[:3])}"
                else:
                    return False, "Ollama running but no models installed"
            else:
                return False, f"API returned status {response.status_code}"
        except httpx.ConnectError:
            return False, f"Cannot connect to Ollama at {self.base_url}"
        except Exception as e:
            return False, f"Health check failed: {str(e)}"
    
    def list_models(self) -> list:
        """List available models in Ollama."""
        try:
            response = self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m.get("name", "") for m in models]
            return []
        except Exception:
            return []


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
