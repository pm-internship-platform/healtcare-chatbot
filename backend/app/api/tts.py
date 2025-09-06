# backend/app/api/tts.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from pathlib import Path
from ..services.tts_service import TTSService
from ..utils.logger import log_info, log_error

router = APIRouter(prefix="/tts", tags=["TTS"])

class TTSRequest(BaseModel):
    text: str
    language: str = "en"

@router.post("")
async def text_to_speech(request: TTSRequest):
    tts_service = TTSService()
    
    try:
        # Generate speech
        audio_file = await tts_service.text_to_speech(request.text, request.language)
        
        if audio_file and os.path.exists(audio_file):
            # Return the audio file
            return FileResponse(
                audio_file,
                media_type="audio/mpeg",
                filename="speech.mp3"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate speech")
            
    except Exception as e:
        log_error(f"TTS API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating speech")
    finally:
        # Clean up the file after sending
        if audio_file and os.path.exists(audio_file):
            await tts_service.cleanup_file(audio_file)