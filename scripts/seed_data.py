#!/usr/bin/env python3
"""
Script to populate MongoDB with initial health and quiz data
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from app.db.mongo import connect_to_mongo, quizzes_collection, users_collection
from app.utils.logger import setup_logging, log_info

async def seed_quiz_data():
    """Seed initial quiz data"""
    quizzes = [
        {
            "title": "General Health Knowledge",
            "description": "Test your general health knowledge",
            "questions": [
                {
                    "question": "What is the primary symptom of dengue fever?",
                    "options": [
                        "High fever and severe headache",
                        "Cough and cold",
                        "Joint pain and swelling",
                        "Skin rashes only"
                    ],
                    "correct_answer": "High fever and severe headache"
                },
                {
                    "question": "How can malaria be prevented?",
                    "options": [
                        "Using mosquito nets",
                        "Drinking boiled water",
                        "Washing hands regularly",
                        "Avoiding crowded places"
                    ],
                    "correct_answer": "Using mosquito nets"
                },
                {
                    "question": "At what age should a child receive the measles vaccine?",
                    "options": [
                        "At birth",
                        "6 months",
                        "9 months",
                        "1 year"
                    ],
                    "correct_answer": "9 months"
                }
            ],
            "difficulty": "easy",
            "category": "general_health"
        },
        {
            "title": "Nutrition Knowledge",
            "description": "Test your nutrition knowledge",
            "questions": [
                {
                    "question": "Which vitamin is essential for strong bones?",
                    "options": [
                        "Vitamin A",
                        "Vitamin C",
                        "Vitamin D",
                        "Vitamin K"
                    ],
                    "correct_answer": "Vitamin D"
                },
                {
                    "question": "What is the main source of protein for vegetarians?",
                    "options": [
                        "Rice",
                        "Lentils and pulses",
                        "Vegetables",
                        "Fruits"
                    ],
                    "correct_answer": "Lentils and pulses"
                }
            ],
            "difficulty": "medium",
            "category": "nutrition"
        }
    ]
    
    # Clear existing quizzes
    await quizzes_collection.delete_many({})
    
    # Insert new quizzes
    result = await quizzes_collection.insert_many(quizzes)
    log_info(f"Inserted {len(result.inserted_ids)} quizzes")
    
    return result.inserted_ids

async def seed_sample_users():
    """Seed sample user data"""
    users = [
        {
            "user_id": "user_001",
            "phone": "+919876543210",
            "district": "Bhubaneswar",
            "language": "en",
            "age": 28,
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "user_id": "user_002",
            "phone": "+919876543211",
            "district": "Cuttack",
            "language": "or",
            "age": 35,
            "created_at": "2024-01-16T11:45:00Z"
        }
    ]
    
    # Clear existing users
    await users_collection.delete_many({})
    
    # Insert new users
    result = await users_collection.insert_many(users)
    log_info(f"Inserted {len(result.inserted_ids)} sample users")
    
    return result.inserted_ids

async def main():
    """Main function to seed all data"""
    setup_logging()
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        log_info("Connected to MongoDB")
        
        # Seed data
        quiz_ids = await seed_quiz_data()
        user_ids = await seed_sample_users()
        
        log_info("Data seeding completed successfully!")
        log_info(f"Quiz IDs: {quiz_ids}")
        log_info(f"User IDs: {user_ids}")
        
    except Exception as e:
        log_info(f"Error seeding data: {str(e)}")
        raise
    finally:
        # Close connection
        from app.db.mongo import close_mongo_connection
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())