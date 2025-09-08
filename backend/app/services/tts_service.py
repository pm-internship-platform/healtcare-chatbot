# backend/app/services/tts_service.py
from gtts import gTTS
import os
import tempfile
from pathlib import Path
from ..utils.logger import log_info, log_error

class TTSService:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    async def text_to_speech(self, text: str, language: str = "en"):
        """
        Convert text to speech using gTTS and return the audio file path
        """
        try:
            # Map language codes to gTTS compatible codes
            lang_map = {
                "en": "en",
                "en-IN": "en",
                "hi": "hi",
                "hi-IN": "hi",
                "or": "or",  # Odia
                "or-IN": "or"
            }
            
            tts_lang = lang_map.get(language, "en")
            
            # Create gTTS object
            tts = gTTS(text=text, lang=tts_lang, slow=False)
            
            # Save to temporary file
            temp_file = Path(self.temp_dir) / f"tts_{hash(text)}.mp3"
            tts.save(str(temp_file))
            
            log_info(f"Generated TTS for {len(text)} characters in {tts_lang}")
            return str(temp_file)
            
        except Exception as e:
            log_error(f"TTS generation error: {str(e)}")
            return None
    
    async def cleanup_file(self, file_path: str):
        """
        Clean up temporary audio files
        """
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            log_error(f"File cleanup error: {str(e)}")