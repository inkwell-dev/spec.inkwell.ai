# 📚 Inkwell — Product Specifications

Welcome to the **Inkwell specification repository**.

This repository contains all the documentation required to understand, design, and build the Inkwell platform — an **AI-powered writing marketplace** connecting independent writers with magazine publishers.

Each document covers a specific aspect of the system, from product vision to technical architecture.

---

## 🎯 Project Snapshot (2026-05-21)

Inkwell is a two-sided platform:

- **Writers** produce articles with AI assistance (chat, voice, inline editing), and can list published articles for licensing
- **Magazines** browse writers, evaluate them via decision-support analytics + AI-generated Portfolio Insights, then license articles for their curated library

The defining differentiator is **RAG used twice**: once to help writers ("AI writes like me") and once to help magazines ("AI tells me what this writer is great at").

---

## 🧭 How to Navigate

Start from the **Product Overview** for vision, then move through Features and Flows, then dive into architecture and data layers.

If you want to track build progress, see the **Phase Plan**.

---

## 📄 Specification Index

### 🗺️ Build Plan
- [00 - Phase Plan (checkboxes)](./0-phase-plan.md)

### 🧠 Product & Vision
- [01 - Product Overview](./1-product-overview.md)

### 📋 Features & User Experience
- [02 - Features](./2-features.md)
- [03 - User Flows](./3-user-flows.md)

### 🏗️ Architecture & AI
- [04 - System Architecture](./4-system-architecture.md)
- [05 - AI Design](./5-ai-design.md)

### 🗄️ Data
- [06 - Database Schema](./6-database-schema.md)

### 📊 Analytics
- [07 - Analytics Model](./7-analytics-model.md)

### 🚀 DevOps
- [08 - DevOps](./8-devops.md)

---

## 🧩 Repository Structure

```bash
spec.inkwell.ai/
├── 0-phase-plan.md
├── 1-product-overview.md
├── 2-features.md
├── 3-user-flows.md
├── 4-system-architecture.md
├── 5-ai-design.md
├── 6-database-schema.md
├── 7-analytics-model.md
└── 8-devops.md
```
