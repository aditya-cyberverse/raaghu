import os
import requests
from groq import Groq

class LLMProvider:
    def __init__(self, ollama_model="qwen2.5-coder:3b"):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = ollama_model
        
        # Groq client (reads GROQ_API_KEY from environment or fallback string)
        groq_key = os.getenv("GROQ_API_KEY", "")
        self.groq_client = Groq(api_key=groq_key) if groq_key else None

    def query_ollama(self, prompt: str, system: str = "") -> str:
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "system": system,
            "stream": False
        }
        try:
            res = requests.post(self.ollama_url, json=payload, timeout=120)
            res.raise_for_status()
            return res.json().get("response", "")
        except Exception as e:
            return f"[Error: Ollama unreachable - {e}]"

    def query_cloud_manager(self, prompt: str, system: str = "") -> str:
        if not self.groq_client:
            # Fallback to local if no API key is present
            return self.query_ollama(prompt, system)
        
        try:
            completion = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[Error: Cloud inference failed - {e}]"
