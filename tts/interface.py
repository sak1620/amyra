from abc import ABC, abstractmethod
from typing import Generator, Optional
import numpy as np

class TTSEngine(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> Generator[np.ndarray, None, None]:
        """Convert text to speech audio chunks."""
        pass

    @abstractmethod
    def stop(self):
        """Interrupt synthesis if running."""
        pass
