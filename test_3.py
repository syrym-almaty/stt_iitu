from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import time

# Ensure to install the required package before running:
# pip install transformers tqdm

# Set paths
TRANSCRIPTION_FILE_PATH = r"C:\Users\syrym\Downloads\АСИИН\transcription.txt"

# Load MarianMT model and tokenizer for Russian to English translation
model_name = "Helsinki-NLP/opus-mt-ru-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Function to translate Russian text to English using Hugging Face Model
def translate_russian_to_english(russian_text):
    tokens = tokenizer([russian_text], return_tensors="pt", padding=True)
    translated_tokens = model.generate(**tokens)
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return translated_text

# Read transcription from file
with open(TRANSCRIPTION_FILE_PATH, "r", encoding="utf-8") as f:
    transcript = f.read()

# Split the transcript into smaller chunks to avoid model input length limits
CHUNK_SIZE = 400  # Adjust chunk size if needed
chunks = [transcript[i:i + CHUNK_SIZE] for i in range(0, len(transcript), CHUNK_SIZE)]

# Add patience bar for translation process
print("Translating text...")
translated_chunks = []
for chunk in tqdm(chunks, desc="Translation in Progress", unit="chunk"):
    translated_chunks.append(translate_russian_to_english(chunk))

# Combine translated chunks
english_translation = " ".join(translated_chunks)

print("Translated Text:")
print(english_translation)

# Optionally, save the translated text to a file
translated_file_path = TRANSCRIPTION_FILE_PATH.rsplit('.', 1)[0] + "_translated.txt"
with open(translated_file_path, "w", encoding="utf-8") as f:
    f.write(english_translation)

print(f"Translated text saved to {translated_file_path}")