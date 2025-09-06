# backend/app/api/chat.py (updated with fallback)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..services.rasa_client import RasaClient
from ..services.openrouter_client import OpenRouterClient
from ..services.fallback_responder import FallbackResponder
from ..models.conversation import save_conversation
from ..utils.logger import log_info, log_error
from ..utils.encryption import anonymize_user_id

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    language: str = "en-IN"

class ChatResponse(BaseModel):
    response: str
    language: str
    source: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        anon_user_id = anonymize_user_id(request.user_id) if request.user_id else "anonymous"
        
        rasa_client = RasaClient()
        openrouter = OpenRouterClient()
        fallback_responder = FallbackResponder()
        
        user_message = request.message
        
        # Try Rasa first
        try:
            rasa_response = await rasa_client.send_message(user_message)
            
            if (rasa_response.get("confidence", 0) >= 0.6 and 
                rasa_response.get("intent", {}).get("name") not in ["out_of_scope", "nlu_fallback"]):
                
                final_response = rasa_response.get("text", "")
                source = "rasa"
                
                # Try to save conversation
                try:
                    await save_conversation(
                        user_id=anon_user_id,
                        message=request.message,
                        response=final_response,
                        language=request.language,
                        source=source
                    )
                except Exception as e:
                    log_error(f"Failed to save conversation: {str(e)}")
                
                log_info(f"Chat processed for user {anon_user_id}, source: {source}")
                
                return ChatResponse(
                    response=final_response,
                    language=request.language,
                    source=source
                )
                
        except Exception as e:
            log_error(f"RASA error: {str(e)}")
            # Continue to next option
        
        # Try OpenRouter/Gemini
        try:
            gemini_response = await openrouter.generate_response(
                prompt=f"As a health assistant for Odisha, answer: {user_message}"
            )
            
            final_response = gemini_response
            source = "gemini"
            
            # Try to save conversation
            try:
                await save_conversation(
                    user_id=anon_user_id,
                    message=request.message,
                    response=final_response,
                    language=request.language,
                    source=source
                )
            except Exception as e:
                log_error(f"Failed to save conversation: {str(e)}")
            
            log_info(f"Chat processed for user {anon_user_id}, source: {source}")
            
            return ChatResponse(
                response=final_response,
                language=request.language,
                source=source
            )
            
        except Exception as e:
            log_error(f"OpenRouter error: {str(e)}")
            # Continue to fallback
        
        # Use fallback responder
        final_response = await fallback_responder.get_response(user_message)
        source = "fallback"
        
        # Try to save conversation
        try:
            await save_conversation(
                user_id=anon_user_id,
                message=request.message,
                response=final_response,
                language=request.language,
                source=source
            )
        except Exception as e:
            log_error(f"Failed to save conversation: {str(e)}")
        
        log_info(f"Chat processed for user {anon_user_id}, source: {source}")
        
        return ChatResponse(
            response=final_response,
            language=request.language,
            source=source
        )
        
    except Exception as e:
        log_error(f"Chat processing error: {str(e)}")
        # Ultimate fallback
        return ChatResponse(
            response="I apologize, but I'm experiencing technical difficulties. Please try again later or contact your local health center for immediate assistance.",
            language=request.language,
            source="error"
        )