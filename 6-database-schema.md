# 06 - Database Schema

## 1. Overview

This document defines the database schema for the AI-powered writing platform.

The system uses a relational database (PostgreSQL) to store structured data, with support for JSON fields and future vector extensions.

The schema is designed to:
- Ensure data consistency
- Support scalability
- Enable efficient querying
- Handle analytics and AI interactions

---

## 2. Design Principles

- Normalized structure for core entities
- Use of foreign keys for relationships
- Use of indexes for performance
- Separation of transactional data and analytics events
- Support for extensibility (AI, analytics, premium features)

---

## 3. Core Entities

### 3.1 Users

Represents all platform users.

Fields:
- id (UUID, PK)
- email (string, unique)
- password_hash (string, nullable for OAuth)
- provider (string, e.g. "local", "google")
- role (enum: guest, reader, writer, admin)
- subscription_type (enum: free_reader, premium_reader, free_writer, premium_writer)
- ai_tokens (integer)
- name (string)
- bio (text)
- avatar_url (string)
- created_at (timestamp)
- updated_at (timestamp)

Indexes:
- email (unique)

---

### 3.2 Articles

Represents written content.

Fields:
- id (UUID, PK)
- author_id (UUID, FK → users.id)
- title (string)
- excerpt (text)
- content (JSON or rich text format)
- thumbnail_url (string)
- status (enum: draft, published)
- visibility (enum: free, premium)
- read_time (integer, estimated minutes)
- created_at (timestamp)
- updated_at (timestamp)
- published_at (timestamp, nullable)

Indexes:
- author_id
- status
- visibility

---

### 3.3 Comments

Supports threaded comments.

Fields:
- id (UUID, PK)
- article_id (UUID, FK → articles.id)
- user_id (UUID, FK → users.id)
- parent_id (UUID, FK → comments.id, nullable)
- content (text)
- created_at (timestamp)

Indexes:
- article_id
- parent_id

---

### 3.4 Likes

Tracks article likes.

Fields:
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- article_id (UUID, FK → articles.id)
- created_at (timestamp)

Constraints:
- unique (user_id, article_id)

Indexes:
- article_id

---

### 3.5 Follows

Tracks user relationships.

Fields:
- id (UUID, PK)
- follower_id (UUID, FK → users.id)
- following_id (UUID, FK → users.id)
- created_at (timestamp)

Constraints:
- unique (follower_id, following_id)

Indexes:
- follower_id
- following_id

---

### 3.6 Reposts

Tracks reposted articles.

Fields:
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- article_id (UUID, FK → articles.id)
- created_at (timestamp)

Constraints:
- unique (user_id, article_id)

---

## 4. AI-Related Entities

### 4.1 AI Interactions

Stores AI usage history.

Fields:
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- article_id (UUID, FK → articles.id, nullable)
- action_type (enum: chat, rewrite, expand, shorten, voice)
- input_text (text)
- output_text (text)
- tokens_used (integer)
- created_at (timestamp)

Indexes:
- user_id
- article_id

---

### 4.2 User AI Memory

Stores user preferences for personalization.

Fields:
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- preferences (JSON)
- updated_at (timestamp)

---

## 5. Analytics Entities

### 5.1 Analytics Events

Stores raw user activity.

Fields:
- id (UUID, PK)
- user_id (UUID, FK → users.id, nullable)
- article_id (UUID, FK → articles.id)
- event_type (enum: view, scroll, like)
- metadata (JSON)
- created_at (timestamp)

Indexes:
- article_id
- event_type

---

### 5.2 Article Metrics (Aggregated)

Stores computed analytics.

Fields:
- id (UUID, PK)
- article_id (UUID, FK → articles.id)
- total_views (integer)
- total_likes (integer)
- avg_read_time (float)
- engagement_rate (float)
- updated_at (timestamp)

---

## 6. Notification System

### 6.1 Notifications

Stores user notifications.

Fields:
- id (UUID, PK)
- user_id (UUID, FK → users.id)
- type (enum: follow, like, comment)
- data (JSON)
- is_read (boolean)
- created_at (timestamp)

Indexes:
- user_id
- is_read

---

## 7. Moderation System

### 7.1 Reports

Stores reported content or users.

Fields:
- id (UUID, PK)
- reporter_id (UUID, FK → users.id)
- target_type (enum: article, user)
- target_id (UUID)
- reason (text)
- status (enum: pending, reviewed, resolved)
- created_at (timestamp)

Indexes:
- target_type
- status

---

## 8. Relationships Summary

- A user can create many articles  
- An article belongs to one user  
- An article has many comments  
- Comments can have parent-child relationships  
- Users can like many articles  
- Users can follow other users  
- Users generate analytics events  
- Users interact with AI  

---

## 9. Constraints and Integrity

- Foreign key constraints enforced on all relations  
- Unique constraints prevent duplicate likes, follows, reposts  
- Cascading deletes (optional for cleanup strategy)  

---

## 10. Performance Considerations

- Index frequently queried fields (user_id, article_id)  
- Use pagination for large datasets  
- Separate analytics aggregation from transactional queries  

---

## 11. Future Extensions

- Vector embeddings for semantic search  
- Tagging system for articles  
- Bookmark system  
- Advanced AI logs and evaluation  

---

## Summary

The database schema is designed to support:

- Core platform features (articles, users, social interactions)  
- AI integration (interactions, memory)  
- Analytics tracking and aggregation  
- Scalability and performance optimization  

It provides a strong foundation for both MVP and future enhancements.
