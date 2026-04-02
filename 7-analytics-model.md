# 07 - Analytics Model

## 1. Overview

This document defines the analytics system used to track, process, and analyze user interactions with articles.

The goal of the analytics model is to:

- Measure reader engagement  
- Provide actionable insights to writers  
- Support AI-driven feedback  
- Enable future data-driven optimizations  

---

## 2. Analytics Objectives

The analytics system must:

- Track how users interact with articles  
- Identify engagement patterns  
- Detect where users drop off  
- Provide clear metrics to writers  
- Enable future AI-based analysis  

---

## 3. Event-Based Tracking Model

The system uses an **event-driven architecture**.

Each user interaction generates an event that is stored and later processed.

---

## 4. Event Types

### 4.1 View Event

Triggered when a user opens an article.

Captured data:
- article_id  
- user_id (nullable)  
- timestamp  
- device (optional)  

---

### 4.2 Scroll Event

Triggered as the user scrolls through the article.

Captured data:
- article_id  
- user_id (nullable)  
- paragraph_index  
- scroll_percentage  
- timestamp  

---

### 4.3 Time Tracking

Measures how long a user stays on an article.

Captured data:
- article_id  
- user_id (nullable)  
- session_duration  
- timestamp  

---

### 4.4 Like Event

Triggered when a user likes an article.

Captured data:
- article_id  
- user_id  
- timestamp  

---

## 5. Event Flow

User Interaction  
→ Frontend captures event  
→ Event sent to backend  
→ Stored in database  
→ Processed asynchronously  
→ Aggregated into metrics  

---

## 6. Data Storage Strategy

### 6.1 Raw Events

Stored in:
- analytics_events table  

Purpose:
- Full history of interactions  
- Used for detailed analysis  

---

### 6.2 Aggregated Metrics

Stored in:
- article_metrics table  

Purpose:
- Fast access for dashboards  
- Precomputed values  

---

## 7. Key Metrics

### 7.1 Total Views

Number of times an article is opened.

---

### 7.2 Average Read Time

Average duration users spend reading an article.

---

### 7.3 Scroll Depth

Measures how far users scroll.

Types:
- Average scroll percentage  
- Maximum scroll reached  

---

### 7.4 Engagement Rate

Calculated as:

engagement_rate = (users who read most of the article) / total views  

---

### 7.5 Drop-off Points

Identifies where users stop reading.

Based on:
- Scroll events  
- Paragraph index  

---

### 7.6 Likes Count

Total number of likes per article.

---

## 8. Paragraph-Level Analytics

Each paragraph is treated as a unit of analysis.

Tracked data:
- paragraph_index  
- number of views  
- average time spent  
- drop-off rate  

---

## 9. Analytics Processing

### 9.1 Aggregation Jobs

Background jobs compute:

- Views per article  
- Average read time  
- Scroll distribution  
- Engagement rate  

---

### 9.2 Processing Frequency

- Near real-time (basic updates)  
- Batch processing (periodic aggregation)  

---

## 10. Writer Dashboard

Writers can view:

- Total views  
- Read time  
- Scroll depth  
- Engagement indicators  
- Likes  

---

## 11. AI Feedback Integration

Analytics data is used to generate insights:

Examples:
- "Users drop off at paragraph 3"  
- "Your intro has low engagement"  
- "Article is too long compared to average read time"  

---

## 12. Performance Considerations

- Use batching for event storage  
- Avoid excessive event frequency  
- Index analytics tables  
- Use aggregation tables for fast queries  

---

## 13. Privacy Considerations

- user_id can be nullable for anonymous users  
- Avoid storing sensitive personal data  
- Respect user privacy regulations  

---

## 14. Future Enhancements

- Heatmaps for visual engagement  
- Real-time analytics dashboard  
- Cohort analysis  
- A/B testing support  
- AI-driven recommendations  

---

## Summary

The analytics model provides:

- Fine-grained tracking of user behavior  
- Aggregated insights for performance  
- A foundation for AI-driven improvements  

It enables the platform to evolve into a data-driven content ecosystem.
