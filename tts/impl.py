from tts.interface import TTSEngine
from typing import Generator
import numpy as np
import pyttsx3
import tempfile
import os

class Pyttsx3TTS(TTSEngine):
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set properties for faster endpointing if possible
        self.engine.setProperty('rate', 150) 

    def synthesize(self, text: str) -> Generator[np.ndarray, None, None]:
        # pyttsx3 is hard to stream chunks from directly as audio data.
        # It usually plays directly or saves to file.
        # For MVP, we can save to file and read it, or use the 'save_to_file' and yield chunks.
        # However, pyttsx3's save_to_file adds headers.
        
        # PROVISIONAL: Since pyttsx3 is blocking/event loop based, it's tricky to yield chunks *while* synthesis happens without diving deep.
        # Alternative: We can synthesize sentences.
        
        # For now, let's implement a "whole" synthesis or use a temp file.
        # We need to return np.ndarray chunks.
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            fname = fp.name
            
        self.engine.save_to_file(text, fname)
        self.engine.runAndWait()
        
        # Read the file
        # Helper to read wav (numpy/scipy)
        import scipy.io.wavfile as wav
        fs, data = wav.read(fname)
        
        # Yield the whole thing or chunks
        # If stereo, convert to mono
        if len(data.shape) > 1:
            data = data.mean(axis=1)
            
        # Yield in chunks of e.g. 10ms or more
        chunk_size = int(fs * 0.1) # 100ms
        for i in range(0, len(data), chunk_size):
            yield data[i:i+chunk_size].astype(np.float32) / 32768.0

        os.remove(fname)

    def stop(self):
        self.engine.stop()
