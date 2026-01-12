from abc import ABC, abstractmethod
import numpy as np
from typing import Generator, Optional

class STTEngine(ABC):
    @abstractmethod
    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio data to text."""
        pass
