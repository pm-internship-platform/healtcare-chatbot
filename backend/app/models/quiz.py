from bson import ObjectId
from datetime import datetime
from ..db.mongo import quiz_results_collection, quizzes_collection
from ..utils.logger import log_info, log_error

async def save_quiz_result(user_id: str, quiz_id: str, score: int, badge: str):
    try:
        result = {
            "user_id": user_id,
            "quiz_id": quiz_id,
            "score": score,
            "badge": badge,
            "timestamp": datetime.utcnow()
        }
        await quiz_results_collection.insert_one(result)
        log_info(f"Quiz result saved for user {user_id}")
        return True
    except Exception as e:
        log_error(f"Quiz result save error: {str(e)}")
        return False

async def get_quiz_results(user_id: str):
    try:
        results = await quiz_results_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).to_list(length=50)
        return results
    except Exception as e:
        log_error(f"Quiz results fetch error: {str(e)}")
        return []

async def get_quiz_questions(quiz_id: str):
    try:
        quiz = await quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
        return quiz
    except Exception as e:
        log_error(f"Quiz questions fetch error: {str(e)}")
        return None

async def get_all_quizzes():
    try:
        quizzes = await quizzes_collection.find().to_list(length=20)
        return quizzes
    except Exception as e:
        log_error(f"Quizzes fetch error: {str(e)}")
        return []