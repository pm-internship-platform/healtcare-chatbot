# System Architecture

## Overview
The AI Health Chatbot is a hybrid AI system that combines rule-based processing with generative AI to provide accurate health information to users in Odisha.

## Architecture Components

### 1. Frontend Layer
- **Web Interface**: WhatsApp/ChatGPT-like UI built with HTML, CSS, and JavaScript
- **Voice Support**: Web Speech API for multilingual voice input/output
- **Responsive Design**: TailwindCSS with daisyUI for mobile-friendly interface
- **Offline Support**: Service workers and cached responses

### 2. Backend Layer (FastAPI)
- **RESTful API**: FastAPI framework with async/await support
- **Authentication**: User session management with anonymization
- **Rate Limiting**: Request throttling to prevent abuse
- **CORS Support**: Cross-origin resource sharing for frontend integration

### 3. AI/NLP Layer
- **Rasa NLP**: Intent classification and entity extraction
- **Gemini API**: Generative responses for complex queries
- **Hybrid Approach**: Rule-based responses for common queries, generative for complex ones

### 4. Data Layer
- **MongoDB**: NoSQL database for user data, conversations, and quiz results
- **Caching**: Redis-like offline caching for frequently accessed data
- **Data Privacy**: User data anonymization and encryption

### 5. Integration Layer
- **Government APIs**: Real-time health data integration
- **Bhashini API**: Multilingual translation support
- **Twilio API**: WhatsApp/SMS messaging capabilities
- **OpenRouter API**: Gemini model access

### 6. Analytics Layer
- **Predictive Models**: Machine learning for outbreak predictions
- **Monitoring**: Service health checks and performance metrics
- **Logging**: Comprehensive logging for debugging and analysis

## Data Flow

1. User sends message (text/voice) → Frontend
2. Frontend → Backend API (/api/chat)
3. Backend → Rasa (intent classification)
4. If confidence high → Rasa response
5. If confidence low → Gemini API → Response
6. If translation needed → Bhashini API
7. Response → User + Database storage
8. Analytics → Monitoring and prediction updates

## Security Features
- Data anonymization for user privacy
- HTTPS encryption for all communications
- Input validation and sanitization
- Rate limiting and abuse prevention
- Regular security updates and patches

## Scalability
- Horizontal scaling with load balancers
- Database replication and sharding
- CDN for static assets
- Async processing for heavy operations