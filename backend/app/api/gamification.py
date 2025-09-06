from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from ..models.quiz import save_quiz_result, get_quiz_results, get_quiz_questions
from ..models.user import get_user_by_id
from ..services.sms_whatsapp import send_whatsapp_message
from ..services.bhashini_client import BhashiniClient
from ..utils.logger import log_info, log_error
from ..utils.encryption import anonymize_user_id

router = APIRouter(prefix="/gamification", tags=["Gamification"])

class QuizRequest(BaseModel):
    user_id: str
    quiz_id: str
    answers: List[str]
    language: str = "en-IN"

class QuizResponse(BaseModel):
    quiz_id: str
    score: int
    total_questions: int
    badge: str
    message: str

@router.post("/quiz", response_model=QuizResponse)
async def submit_quiz(request: QuizRequest):
    try:
        anon_user_id = anonymize_user_id(request.user_id)
        bhashini = BhashiniClient()
        
        quiz = await get_quiz_questions(request.quiz_id)
        if not quiz:
            log_error(f"Quiz {request.quiz_id} not found")
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        correct_answers = quiz["correct_answers"]
        if len(request.answers) != len(correct_answers):
            log_error(f"Invalid number of answers for quiz {request.quiz_id}")
            raise HTTPException(status_code=400, detail="Invalid number of answers")
        
        score = sum(1 for user_ans, correct_ans in zip(request.answers, correct_answers) 
                    if user_ans.lower() == correct_ans.lower())
        total_questions = len(correct_answers)
        score_percentage = (score / total_questions) * 100
        
        if score_percentage >= 90:
            badge = "Health Champion"
        elif score_percentage >= 80:
            badge = "Health Hero"
        elif score_percentage >= 60:
            badge = "Health Explorer"
        else:
            badge = "Health Learner"
        
        await save_quiz_result(anon_user_id, request.quiz_id, score, badge)
        log_info(f"Saved quiz result for user {anon_user_id}, quiz {request.quiz_id}, score {score}")
        
        message = f"Congratulations! You scored {score}/{total_questions} and earned the '{badge}' badge!"
        
        if request.language.startswith(('or', 'hi')):
            translated_message = await bhashini.translate(
                text=message, source_lang="en", target_lang=request.language
            )
        else:
            translated_message = message
        
        user = await get_user_by_id(anon_user_id)
        if user and user.get("phone"):
            await send_whatsapp_message(user["phone"], translated_message)
            log_info(f"Sent WhatsApp badge notification to {user['phone']}")
        
        return QuizResponse(
            quiz_id=request.quiz_id,
            score=score,
            total_questions=total_questions,
            badge=badge,
            message=translated_message
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        log_error(f"Quiz submission error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing quiz: {str(e)}")

@router.get("/{user_id}/results")
async def get_user_quiz_results(user_id: str):
    try:
        anon_user_id = anonymize_user_id(user_id)
        results = await get_quiz_results(anon_user_id)
        if not results:
            log_error(f"No quiz results found for user {anon_user_id}")
            raise HTTPException(status_code=404, detail="No quiz results found")
        log_info(f"Fetched quiz results for user {anon_user_id}")
        return {"user_id": anon_user_id, "results": results}
    except HTTPException as e:
        raise e
    except Exception as e:
        log_error(f"Quiz results fetch error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching quiz results: {str(e)}")