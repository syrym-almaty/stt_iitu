import os
import wave
import requests
from vosk import Model, KaldiRecognizer
import json
from tqdm import tqdm

# Ensure to install the required packages before running:
# pip install -r requirements.txt

# Download the model if it doesn't exist
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
MODEL_PATH = "vosk-model-small-ru-0.22"

if not os.path.exists(MODEL_PATH):
    print(f"Downloading the model from {MODEL_URL}...")
    response = requests.get(MODEL_URL)
    with open("model.zip", "wb") as model_file:
        model_file.write(response.content)
    print("Downloaded the model. Please unzip it to continue.")
    exit(1)

# Set the path to the audio file
AUDIO_FILE_PATH = r"C:\Users\syrym\Downloads\АСИИН\asiin.wav"

# Load Vosk model
model = Model(MODEL_PATH)

# Open audio file
wf = wave.open(AUDIO_FILE_PATH, "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 48000]:
    print("Audio file must be WAV format mono PCM.")
    exit(1)

recognizer = KaldiRecognizer(model, wf.getframerate())
recognizer.SetWords(True)

# Recognize speech from audio
transcript = ""
total_frames = wf.getnframes() // 4000

for _ in tqdm(range(total_frames), desc="Processing Audio", unit="chunk"):
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        transcript += result.get("text", "") + "\n"

# Add the final part of the recognition
final_result = json.loads(recognizer.FinalResult())
transcript += final_result.get("text", "") + "\n"

# Print the transcript
print("Transcription Result:")
print(transcript)

# Optionally, save the transcription to a text file
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print("Transcription saved to transcription.txt")