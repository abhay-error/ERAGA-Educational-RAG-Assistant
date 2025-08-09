import logging
import requests
import json
from typing import Dict, Any, Optional, List
import openai
from openai import OpenAI

from .config import config

logger = logging.getLogger(__name__)

class LLMProvider:
    def __init__(self):
        self.config = config.get_llm_config()
        self.provider = self.config.get('provider', 'openrouter')
        self.model = self.config.get('model', 'openai/gpt-4o')
        self.temperature = self.config.get('temperature', 0.7)
        self.max_tokens = self.config.get('max_tokens', 4000)
        
        # Initialize provider-specific configurations
        self._setup_provider()
        
        logger.info(f"LLM Provider initialized: {self.provider} with model {self.model}")
    
    def _setup_provider(self):
        """Setup provider-specific configurations."""
        if self.provider == 'openai':
            api_key = self.config.get('openai', {}).get('api_key', '')
            if api_key:
                openai.api_key = api_key
                self.client = OpenAI(api_key=api_key)
            else:
                logger.warning("OpenAI API key not configured")
        
        elif self.provider == 'openrouter':
            self.openrouter_config = self.config.get('openrouter', {})
        
        elif self.provider == 'local':
            self.local_config = self.config.get('local', {})
        
        elif self.provider == 'anthropic':
            self.anthropic_config = self.config.get('anthropic', {})
        
        elif self.provider == 'cohere':
            self.cohere_config = self.config.get('cohere', {})
    
    def generate_response(self, context: str, query: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using the configured LLM provider."""
        try:
            if self.provider == 'openai':
                return self._generate_openai_response(context, query, system_prompt)
            elif self.provider == 'openrouter':
                return self._generate_openrouter_response(context, query, system_prompt)
            elif self.provider == 'local':
                return self._generate_local_response(context, query, system_prompt)
            elif self.provider == 'anthropic':
                return self._generate_anthropic_response(context, query, system_prompt)
            elif self.provider == 'cohere':
                return self._generate_cohere_response(context, query, system_prompt)
            else:
                logger.error(f"Unsupported LLM provider: {self.provider}")
                return "Error: Unsupported LLM provider"
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"
    
    def _generate_openai_response(self, context: str, query: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using OpenAI."""
        if not hasattr(self, 'client'):
            return "Error: OpenAI client not configured"
        
        try:
            # Prepare messages
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system", 
                    "content": "You are a helpful AI assistant for the School of Engineering at the University of Mysore. Provide accurate and helpful responses based on the context provided."
                })
            
            # Add context and query
            if context:
                messages.append({
                    "role": "user", 
                    "content": f"Context:\n{context}\n\nQuestion: {query}"
                })
            else:
                messages.append({"role": "user", "content": query})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in OpenAI response generation: {e}")
            return f"Error: {str(e)}"
    
    def _generate_openrouter_response(self, context: str, query: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using OpenRouter."""
        try:
            api_key = self.openrouter_config.get('api_key', '')
            base_url = self.openrouter_config.get('base_url', 'https://openrouter.ai/api/v1')
            model = self.openrouter_config.get('model', self.model)  # Use OpenRouter-specific model or fallback to main model
            
            if not api_key:
                return "Error: OpenRouter API key not configured"
            
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system", 
                    "content": "You are a helpful AI assistant for the School of Engineering at the University of Mysore. Provide accurate and helpful responses based on the context provided."
                })
            
            if context:
                messages.append({
                    "role": "user", 
                    "content": f"Context:\n{context}\n\nQuestion: {query}"
                })
            else:
                messages.append({"role": "user", "content": query})
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.openrouter_config.get('referer', 'https://your-site.com'),
                "X-Title": self.openrouter_config.get('title', 'College RAG Assistant')
            }
            
            # Prepare payload
            payload = {
                "model": model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            # Make request
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error in OpenRouter response generation: {e}")
            return f"Error: {str(e)}"
    
    def _generate_local_response(self, context: str, query: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using local model (Ollama/LM Studio)."""
        try:
            base_url = self.local_config.get('base_url', 'http://localhost:11434')
            model_name = self.local_config.get('model_name', 'mistral')
            
            # Prepare messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({
                    "role": "system", 
                    "content": "You are a helpful AI assistant for the School of Engineering at the University of Mysore. Provide accurate and helpful responses based on the context provided."
                })
            
            if context:
                messages.append({
                    "role": "user", 
                    "content": f"Context:\n{context}\n\nQuestion: {query}"
                })
            else:
                messages.append({"role": "user", "content": query})
            
            # Prepare payload
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": False
            }
            
            # Make request
            response = requests.post(
                f"{base_url}/v1/chat/completions",
                json=payload,
                timeout=120  # Increased timeout for CPU inference
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error in local model response generation: {e}")
            return f"Error: {str(e)}"
    
    def _generate_anthropic_response(self, context: str, query: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using Anthropic Claude."""
        try:
            api_key = self.anthropic_config.get('api_key', '')
            
            if not api_key:
                return "Error: Anthropic API key not configured"
            
            # Prepare message
            if context:
                message = f"Context:\n{context}\n\nQuestion: {query}"
            else:
                message = query
            
            # Prepare payload
            payload = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            # Make request
            headers = {
                "x-api-key": api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Error in Anthropic response generation: {e}")
            return f"Error: {str(e)}"
    
    def _generate_cohere_response(self, context: str, query: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using Cohere."""
        try:
            api_key = self.cohere_config.get('api_key', '')
            
            if not api_key:
                return "Error: Cohere API key not configured"
            
            # Prepare prompt
            if system_prompt:
                prompt = f"{system_prompt}\n\n"
            else:
                prompt = "You are a helpful AI assistant for the School of Engineering at the University of Mysore. Provide accurate and helpful responses based on the context provided.\n\n"
            
            if context:
                prompt += f"Context:\n{context}\n\nQuestion: {query}"
            else:
                prompt += query
            
            # Prepare payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "k": 0,
                "stop_sequences": [],
                "return_likelihoods": "NONE"
            }
            
            # Make request
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.cohere.ai/v1/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data['generations'][0]['text']
            
        except Exception as e:
            logger.error(f"Error in Cohere response generation: {e}")
            return f"Error: {str(e)}"
