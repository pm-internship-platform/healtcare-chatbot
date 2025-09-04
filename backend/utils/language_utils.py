# app/utils/language_utils.py
# Lightweight helpers for language detection / translation.
# For production, integrate fasttext/langdetect or external translator APIs.

def detect_language(text: str) -> str:
    # naive heuristics — replace with a real detector when needed
    if any("\u0B80" <= ch <= "\u0DFF" for ch in text):  # Indic scripts rough check
        return "unknown-indic"
    return "en"
