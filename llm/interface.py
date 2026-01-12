from abc import ABC, abstractmethod
from typing import Generator, Optional

class LLMEngine(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        """Generate a response from the LLM, streaming tokens."""
        pass
