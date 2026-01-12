from abc import ABC, abstractmethod
from typing import Dict, Any

class EmotionEngine(ABC):
    @abstractmethod
    def detect(self, text: str, audio_features: Any = None) -> Dict[str, Any]:
        """Detect intent and emotion from text (and optional audio)."""
        pass
