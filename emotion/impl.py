from emotion.interface import EmotionEngine
from typing import Dict, Any

class HeuristicEmotion(EmotionEngine):
    def detect(self, text: str, audio_features: Any = None) -> Dict[str, Any]:
        """
        Simple heuristic emotion detection.
        MVP: Rule-based.
        """
        text = text.lower()
        emotion = "neutral"
        intent = "unknown"

        # Simple keyword matching
        if any(w in text for w in ["happy", "great", "good", "love", "awesome"]):
            emotion = "happy"
        elif any(w in text for w in ["sad", "bad", "sorry", "hate", "terrible"]):
            emotion = "sad"
        elif any(w in text for w in ["angry", "mad", "furious"]):
            emotion = "angry"
            
        # Intent (very basic)
        if "?" in text or any(w in text for w in ["what", "who", "where", "when", "why", "how"]):
            intent = "question"
        elif any(w in text for w in ["stop", "pause", "halt"]):
            intent = "stop"
        
        return {
            "emotion": emotion,
            "intent": intent,
            "text": text
        }
