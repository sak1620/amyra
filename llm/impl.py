from llm.interface import LLMEngine
from typing import Generator, Optional
import ollama

class OllamaLLM(LLMEngine):
    def __init__(self, model: str = "llama3.1:8b"):
        self.model = model
        # Ensure ollama is reachable? usually localhost:11434
        # We assume the user has 'ollama' running.

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = ollama.chat(
            model=self.model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
