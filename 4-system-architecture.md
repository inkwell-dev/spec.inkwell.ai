# 04 - System Architecture

## 1. Overview

This document describes the overall system architecture of the AI-powered writing platform.

The system is designed to be:
- Modular  
- Scalable  
- Maintainable  
- AI-ready  

It follows a hybrid microservices architecture, separating core business logic from AI processing.

---

## 2. High-Level Architecture

The system is composed of the following main components:

- Frontend Application  
- Backend API (Core System)  
- AI Processing Service  
- Database Layer  
- Caching & Queue System  
- External Services  

---

## 3. Architecture Diagram

[ Client (Browser) ]
        |
        v
[ Frontend (Next.js) ]
        |
        v
[ Backend API (NestJS) ]
        |
   -------------------------
   |           |           |
   v           v           v
[Auth]     [Core API]   [Notifications]
                    |
                    v
            [ AI Service (Python) ]
                    |
        -------------------------
        |                       |
        v                       v
[ PostgreSQL (Main DB) ]   [ Vector Storage ]
        |
        v
[ Redis (Cache + Queue) ]

---

## 4. Frontend Layer

### Responsibilities

- User interface rendering  
- Rich text editor integration  
- AI interaction (chat, inline editing)  
- State management  
- API communication  

---

### Key Modules

- Authentication UI  
- Article Editor  
- AI Assistant Panel  
- Analytics Dashboard  
- Feed & Article Viewer  

---

### Communication

- REST API calls to backend  
- WebSocket support (optional for future real-time features)  

---

## 5. Backend Layer (Core API)

### Responsibilities

- Business logic  
- Authentication & authorization  
- Article management  
- Social features (likes, comments, follows)  
- Analytics processing  
- Communication with AI service  

---

### Modular Structure

- Auth Module
- Users Module (personal + magazine profiles)
- Articles Module (incl. tags, slugs, soft deletes)
- Comments Module
- Likes Module
- Follow Module
- Reposts Module
- **Marketplace Module** — listings, browsing, license purchase flow
- **Transactions Module** — wallet ledger, atomic financial operations
- Analytics Module (writer-facing + magazine-facing aggregation)
- AI Gateway Module (chat, inline, voice, Portfolio Insights)
- Storage Module (MinIO uploads)
- Notifications Module (SSE delivery)
- Moderation / Reports Module  

---

### API Design

- RESTful API  
- JSON-based communication  
- JWT-secured endpoints  

---

## 6. AI Service Layer

### Purpose

The AI service is separated from the core backend to:
- Isolate AI complexity  
- Improve scalability  
- Allow independent deployment  

---

### Responsibilities

- Process AI requests (chat, inline editing, generation)  
- Handle prompt construction  
- Manage user context and memory  
- Perform speech-to-text processing  
- Communicate with external AI APIs  

---

### Communication

- Backend → AI Service via HTTP (REST)  
- AI Service → External AI APIs  

---

### Key Pipelines

Text Processing:
- Input text + context → Prompt → AI model → Output  

Voice Processing:
- Audio → Transcription → Prompt → AI model → Structured content  

---

## 7. Data Layer

### Primary Database (PostgreSQL)

Stores:
- Users  
- Articles  
- Comments  
- Likes  
- Follows  
- Analytics events  
- AI interactions  

---

### Vector Storage (Optional / Future)

Used for:
- Semantic search  
- Advanced AI context retrieval  

---

### Data Consistency

- Strong consistency for core entities  
- Eventual consistency for analytics  

---

## 8. Caching & Queue Layer (Redis)

### Purpose

- Improve performance  
- Handle asynchronous processing  
- Manage background jobs  

---

### Use Cases

- AI request queue  
- Rate limiting  
- Caching frequently accessed data  
- Notification dispatching  

---

### Queue Processing

- AI tasks are processed asynchronously  
- Prevents blocking main API  

---

## 9. Analytics Architecture

### Event Collection

Frontend sends events:
- Page view  
- Scroll tracking  
- Time spent  

---

### Processing Flow

Client Event → Backend → Database → Aggregation → Dashboard  

---

### Aggregation Strategy

- Periodic aggregation (batch jobs)  
- Metrics computed per article  

---

## 10. Security Architecture

### Authentication

- JWT-based authentication  
- Access token + refresh token  

---

### Authorization

- Role-based access control (RBAC)  
- Permission checks per endpoint  

---

### Data Protection

- Input validation  
- Sanitization of user-generated content  
- Secure file uploads  

---

## 11. Media Storage

### Image Handling

- Uploaded by users  
- Stored in object storage (S3-compatible)  

---

### Access

- Public URLs for rendering  
- Controlled upload endpoints  

---

## 12. Notification System

### Flow

Event Trigger → Backend → Notification Created → Stored → Delivered  

---

### Types

- Follow notifications  
- Likes  
- Comments  

---

## 13. Deployment Architecture

### Services

- Frontend (Next.js)  
- Backend (NestJS)  
- AI Service (Python)  
- PostgreSQL  
- Redis  

---

### Containerization

- Each service runs in a Docker container  
- Services communicate over an internal network  

---

### Reverse Proxy

- Nginx routes incoming traffic to services  

---

## 14. Scalability Considerations

- Horizontal scaling for backend and AI services  
- Stateless API design  
- Queue-based AI processing  
- Database indexing and optimization  

---

## 15. Failure Handling

- Retry mechanism for AI requests  
- Graceful degradation if AI service fails  
- Logging and monitoring for errors  

---

## 16. Testing Strategy (High-Level)

- Unit tests for backend modules  
- Integration tests for APIs  
- Basic validation for AI responses  

---

## Summary

The system architecture ensures scalability, modularity, and strong AI integration.
