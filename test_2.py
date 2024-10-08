from translate import Translator
from tqdm import tqdm
import time

# Ensure to install the required package before running:
# pip install translate tqdm

# Set paths
TRANSCRIPTION_FILE_PATH = r"C:\Users\syrym\Downloads\АСИИН\transcription.txt"

# Translate Russian text to English using Translator
def translate_russian_to_english(russian_text):
    translator = Translator(from_lang="ru", to_lang="en")
    translated = translator.translate(russian_text)
    return translated

# Read transcription from file
with open(TRANSCRIPTION_FILE_PATH, "r", encoding="utf-8") as f:
    transcript = f.read()

# Split the transcript into smaller chunks to avoid query length limits
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