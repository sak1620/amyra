import sys
import logging
import time
from audio.device import LocalAudioInput, LocalAudioOutput
from stt.impl import FasterWhisperSTT
from llm.impl import OllamaLLM
from tts.impl import Pyttsx3TTS
from emotion.impl import HeuristicEmotion
from orchestrator.engine import Orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("amyra.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AMYRA")

def main():
    logger.info("Initializing Amyra local components...")
    
    try:
        # 1. Audio
        audio_in = LocalAudioInput()
        audio_out = LocalAudioOutput()
        
        # 2. STT
        logger.info("Loading STT Model (this may take a while)...")
        stt = FasterWhisperSTT(model_size="small.en") 
        # Note: If quicker-whisper/faster-whisper isn't installed yet, this will fail. 
        # But we handle imports at top level.
        
        # 3. LLM
        logger.info("Connecting to LLM (Ollama)...")
        # llm = OllamaLLM(model="llama3.1:8b")
        
        # 4. TTS
        logger.info("Initializing TTS...")
        tts = Pyttsx3TTS()
        
        # 5. Emotion
        emotion = HeuristicEmotion()
        
        # 6. Orchestrator
        logger.info("Starting Orchestrator...")
        orchestrator = Orchestrator(audio_in, audio_out, stt, "llm", tts, emotion)
        
        orchestrator.start()
        
        print("\n--- AMYRA LISTENING ---")
        print("Press Ctrl+C to stop.")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping...")
        if 'orchestrator' in locals():
            orchestrator.stop()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical Error: {e}")
        raise

if __name__ == "__main__":
    main()
