# scripts/test_accuracy.py
#!/usr/bin/env python3
"""
Script to validate 80% query accuracy
"""

import requests
import json
import logging
import sys  # Added missing import
from typing import List, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Test queries with expected response patterns
TEST_QUERIES = [
    {
        "query": "What are dengue symptoms?",
        "expected_keywords": ["fever", "headache", "pain", "rash", "nausea"]
    },
    {
        "query": "How to prevent malaria?",
        "expected_keywords": ["mosquito", "net", "repellent", "water", "spray"]
    },
    {
        "query": "Vaccination schedule for children",
        "expected_keywords": ["vaccine", "schedule", "months", "years", "BCG", "measles"]
    },
    {
        "query": "What is COVID-19?",
        "expected_keywords": ["covid", "coronavirus", "symptoms", "pandemic", "vaccine"]
    },
    {
        "query": "How to maintain good hygiene?",
        "expected_keywords": ["wash", "hands", "clean", "sanitizer", "water", "soap"]
    },
    {
        "query": "What are the health alerts in Bhubaneswar?",
        "expected_keywords": ["alert", "outbreak", "warning", "cases", "district"]
    },
    {
        "query": "Tell me about diabetes",
        "expected_keywords": ["sugar", "blood", "insulin", "diet", "exercise"]
    },
    {
        "query": "How to treat fever?",
        "expected_keywords": ["temperature", "medicine", "rest", "fluid", "doctor"]
    },
    {
        "query": "What is nutrition?",
        "expected_keywords": ["food", "diet", "vitamins", "minerals", "healthy"]
    },
    {
        "query": "How to avoid heart disease?",
        "expected_keywords": ["heart", "exercise", "diet", "cholesterol", "blood pressure"]
    }
]

def test_query_accuracy():
    """Test the accuracy of chatbot responses"""
    logging.info("Starting query accuracy test...")
    
    results = []
    base_url = "http://localhost:8000/api/chat"
    
    for i, test_case in enumerate(TEST_QUERIES):
        try:
            logging.info(f"Testing query {i+1}/{len(TEST_QUERIES)}: {test_case['query']}")
            
            response = requests.post(
                base_url,
                json={
                    "message": test_case["query"],
                    "language": "en"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data["response"].lower()
                
                # Check for expected keywords
                found_keywords = []
                for keyword in test_case["expected_keywords"]:
                    if keyword.lower() in response_text:
                        found_keywords.append(keyword)
                
                accuracy = len(found_keywords) / len(test_case["expected_keywords"])
                is_accurate = accuracy >= 0.6  # At least 60% keywords match
                
                results.append({
                    "query": test_case["query"],
                    "response": data["response"],
                    "expected_keywords": test_case["expected_keywords"],
                    "found_keywords": found_keywords,
                    "accuracy": accuracy,
                    "is_accurate": is_accurate
                })
                
                status = "✅" if is_accurate else "❌"
                logging.info(f"{status} Accuracy: {accuracy:.2f} - Found: {found_keywords}")
                
            else:
                logging.error(f"API error: {response.status_code}")
                results.append({
                    "query": test_case["query"],
                    "error": f"API returned {response.status_code}",
                    "is_accurate": False
                })
                
        except Exception as e:
            logging.error(f"Error testing query: {str(e)}")
            results.append({
                "query": test_case["query"],
                "error": str(e),
                "is_accurate": False
            })
        
        # Add small delay between requests
        import time
        time.sleep(1)
    
    return results

def calculate_overall_accuracy(results: List[Dict[str, Any]]) -> float:
    """Calculate overall accuracy percentage"""
    successful_tests = sum(1 for result in results if result.get('is_accurate', False))
    total_tests = len(results)
    
    if total_tests == 0:
        return 0.0
    
    return (successful_tests / total_tests) * 100

def main():
    """Main testing function"""
    logging.info("Starting chatbot accuracy validation...")
    
    try:
        results = test_query_accuracy()
        overall_accuracy = calculate_overall_accuracy(results)
        
        logging.info("\n" + "="*50)
        logging.info(f"OVERALL ACCURACY: {overall_accuracy:.2f}%")
        logging.info("="*50)
        
        # Detailed results
        for i, result in enumerate(results):
            status = "✅" if result.get('is_accurate', False) else "❌"
            logging.info(f"{status} Query {i+1}: {result['query']}")
            if 'accuracy' in result:
                logging.info(f"   Accuracy: {result['accuracy']:.2f}")
            if 'error' in result:
                logging.info(f"   Error: {result['error']}")
        
        # Save results to file
        with open("accuracy_test_results.json", "w") as f:
            json.dump({
                "overall_accuracy": overall_accuracy,
                "test_date": "2024-01-20",
                "results": results
            }, f, indent=2)
        
        logging.info(f"Results saved to accuracy_test_results.json")
        
        # Check if we meet the 80% target
        if overall_accuracy >= 80.0:
            logging.info("🎉 SUCCESS: Achieved 80%+ accuracy target!")
            return True
        else:
            logging.warning("⚠️  WARNING: Did not meet 80% accuracy target")
            return False
            
    except Exception as e:
        logging.error(f"Error during accuracy testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)