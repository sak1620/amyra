from abc import ABC, abstractmethod
import numpy as np

class AudioInput(ABC):
    @abstractmethod
    def start(self):
        """Start capturing audio."""
        pass

    @abstractmethod
    def stop(self):
        """Stop capturing audio."""
        pass

    @abstractmethod
    def read(self) -> np.ndarray:
        """Read a chunk of audio data."""
        pass

class AudioOutput(ABC):
    @abstractmethod
    def play(self, audio_data: np.ndarray, sample_rate: int):
        """Play audio data."""
        pass

    @abstractmethod
    def stop(self):
        """Stop playback immediately."""
        pass
