# API Specification

## Base URL
`http://localhost:8000/api` (Development)
`https://api.yourdomain.com/api` (Production)

## Authentication
Most endpoints require a user ID header:
```http
X-User-ID: user_123