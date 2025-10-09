import aiohttp
import logging
import os
from config.settings import LM_STUDIO_URL, AI_MODEL

class LLMClient:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model = AI_MODEL
        self.session = None
        
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60)
            )
        return self.session
        
    async def generate_response(self, prompt: str, max_tokens: int = 500):
        try:
            session = await self.get_session()
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False
            }
            
            async with session.post(
                f"{self.base_url}/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["text"]
                else:
                    logging.error(f"LM Studio error: {response.status}")
                    return None
                    
        except aiohttp.ClientConnectorError:
            logging.error("Cannot connect to LM Studio server")
            return None
        except Exception as e:
            logging.error(f"LLM error: {str(e)}")
            return None
            
    async def close(self):
        if self.session:
            await self.session.close()

# Глобальный экземпляр
llm_client = LLMClient()