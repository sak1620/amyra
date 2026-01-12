import sounddevice as sd
import numpy as np
from audio.interface import AudioInput, AudioOutput
import queue

class LocalAudioInput(AudioInput):
    def __init__(self, sample_rate: int = 16000, channels: int = 1, device=None):
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device
        self.stream = None
        self.queue = queue.Queue()
        self.running = False

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"Audio Input Status: {status}")
        self.queue.put(indata.copy())

    def start(self):
        if self.running:
            return
        self.running = True
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            device=self.device,
            callback=self._callback,
            dtype='float32' # Whisper usually expects float32
        )
        self.stream.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        # Clear queue
        with self.queue.mutex:
            self.queue.queue.clear()

    def read(self) -> np.ndarray:
        if not self.running:
            return np.array([])
        try:
            return self.queue.get(timeout=0.5)
        except queue.Empty:
            return np.array([])

class LocalAudioOutput(AudioOutput):
    def __init__(self, device=None):
        self.device = device

    def play(self, audio_data: np.ndarray, sample_rate: int):
        # sd.play is asynchronous by default
        sd.play(audio_data, samplerate=sample_rate, device=self.device)
        # We might want to wait or block? 
        # For now, let's keep it async but return control.
        # But wait, if we want to stream out, we might need OutputStream.
        # For "Play audio response locally" and "User to interrupt", 
        # fire-and-forget sd.play is okay mostly as long as stop() kills it.
        pass

    def wait(self):
        sd.wait()

    def stop(self):
        sd.stop()
