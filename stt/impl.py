from stt.interface import STTEngine
import numpy as np
from faster_whisper import WhisperModel
import os

class FasterWhisperSTT(STTEngine):
    def __init__(self, model_size="small.en", device="cpu", compute_type="int8"):
        # "auto" compute_type is usually safe, "int8" is good for CPU.
        # "cpu" or "cuda" depending on hardware. MVP says localhost, usually cpu is safer unless high end.
        # PRD Mentioned: "MVP Implementation: whisper.cpp". Faster-whisper is similar.
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        # faster-whisper expects float32 audio, normalized to [-1, 1].
        # audio_data should be a numpy array.
        
        # If audio is int16, normalize.
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0
            
        segments, info = self.model.transcribe(audio_data, beam_size=5)
        
        text = " ".join([segment.text for segment in segments])
        return text.strip()
