import time
import queue
import threading
import numpy as np
from typing import Optional

from audio.interface import AudioInput, AudioOutput
from stt.interface import STTEngine
from llm.interface import LLMEngine
from tts.interface import TTSEngine
from emotion.interface import EmotionEngine

class Orchestrator:
    def __init__(self, 
                 audio_in: AudioInput, 
                 audio_out: AudioOutput,
                 stt: STTEngine,
                 llm: LLMEngine,
                 tts: TTSEngine,
                 emotion: EmotionEngine):
        self.audio_in = audio_in
        self.audio_out = audio_out
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.emotion = emotion
        
        self.running = False
        self.processing = False
        
        # Buffers
        self.audio_buffer = []
        self.silence_threshold = 0.001 # Extremely low threshold for debugging
        self.silence_duration = 0.0
        self.max_silence = 1.0 # Stop recording after 1s silence

    def start(self):
        self.running = True
        self.audio_in.start()
        # Start input loop
        self.input_thread = threading.Thread(target=self._input_loop)
        self.input_thread.start()

    def stop(self):
        self.running = False
        self.audio_in.stop()
        if self.input_thread:
            self.input_thread.join()

    def _input_loop(self):
        print("Orchestrator Input Loop Started (Debug Mode).")
        recording = False
        silence_start = None
        
        while self.running:
            chunk = self.audio_in.read()
            if chunk.size == 0:
                time.sleep(0.01)
                continue
                
            # Interruption check: If TTS is playing and we detect speech
            # For simplicity, calculate energy
            energy = np.sqrt(np.mean(chunk**2))
            
            # Debugging print to confirm mic is working (only significant energy)
            # if energy > 0.00001:
            #     print(f"DEBUG: Mic Energy: {energy:.6f}")

            if energy > self.silence_threshold:
                # Speech detected
                if not recording:
                    print(f"DEBUG: Speech detected (Energy={energy:.6f}), starting recording...")
                    recording = True
                    self.audio_buffer = []
                    
                    # INTERRUPT TTS
                    self.tts.stop()
                    self.audio_out.stop()
                
                self.audio_buffer.append(chunk)
                silence_start = None
                
            elif recording:
                # Silence during recording
                self.audio_buffer.append(chunk) # Keep recording a bit of silence
                if silence_start is None:
                    silence_start = time.time()
                
                if time.time() - silence_start > self.max_silence:
                    # End of utterance
                    print("End of utterance detected.")
                    recording = False
                    if self.audio_buffer:
                        self._process_utterance(np.concatenate(self.audio_buffer))
                    self.audio_buffer = []
        
    def _process_utterance(self, audio_data: np.ndarray):
        print("Processing utterance...")
        
        # 1. STT
        try:
            text = self.stt.transcribe(audio_data)
            print(f"\n---> HEARD: '{text}' <---")
        except Exception as e:
            print(f"STT Error: {e}")
            return

        if not text.strip():
            return

        # 2. Emotion/Intent
        metadata = self.emotion.detect(text)
        print(f"Metadata: {metadata}")
        
        # 3. LLM
        # We can stream LLM -> TTS
        full_response = ""
        prompt = text 
        
        print("AI Generating...")
        stream = prompt.split(" ") #self.llm.generate(prompt)
        
        # For basic TTS (Pyttsx3 non-streaming), we might need to accumulate sentences.
        # Simple heuristics: split by punctuation.
        buffer = ""
        for token in stream:
            buffer += token
            # Yield on punctuation to stream TTS
            if any(p in buffer for p in [".", "!", "?", "\n"]):
                # Synthesize valid chunk
                print(f"AI chunk: {buffer}")
                self._synthesize_and_play(buffer)
                full_response += buffer
                buffer = ""
        
        if buffer:
            print(f"AI chunk: {buffer}")
            self._synthesize_and_play(buffer)
            full_response += buffer

    def _synthesize_and_play(self, text: str):
        try:
            for audio_chunk in self.tts.synthesize(text):
                self.audio_out.play(audio_chunk, 16000) # Assuming 16k sample rate
        except Exception as e:
            print(f"TTS Error: {e}")
