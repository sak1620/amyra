import sounddevice as sd
import numpy as np

def test_mic():
    print("Listing devices:")
    print(sd.query_devices())
    
    fs = 16000
    duration = 3  # seconds
    
    print(f"\nRecording for {duration} seconds... speak now!")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Finished recording.")
    
    max_val = np.max(np.abs(myrecording))
    mean_val = np.mean(np.abs(myrecording))
    print(f"Max Amplitude: {max_val}")
    print(f"Mean Amplitude: {mean_val}")
    
    if max_val < 0.001:
        print("WARNING: Audio seems silent. Check your microphone settings.")
    else:
        print("Audio detected!")

if __name__ == "__main__":
    test_mic()
