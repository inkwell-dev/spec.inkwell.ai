::: {.titlepage}

**TEK-UP University**

**GLSI (Software Engineering and Information Systems)**

&nbsp;

**End-of-Studies Project Report**

Submitted in partial fulfilment of the requirements for the degree of
**National Engineering Diploma in Computer Science (GLSI)**

&nbsp;

**Inkwell.ai**

**An AI-powered writing marketplace connecting independent writers and magazine publishers**

&nbsp;

Carried out by: **Oussama Bejaoui**

Academic supervisor: **Mr. Bilel Zemzem**

Professional supervisor: **Mr. Ramzy Chridi**

Host organisation: **Intuitiv Group**

&nbsp;

Project period: **1 February 2026 – 31 July 2026**

Academic year **2025–2026**

:::

# Acknowledgements {.unnumbered}

I would like to express my sincere gratitude to my academic supervisor,
**Mr. Bilel Zemzem**, for his guidance, his availability and his valuable advice
throughout this project, and for the rigour he encouraged in both the work and this
report.

I am equally grateful to my professional supervisor, **Mr. Ramzy Chridi**, and to the
whole team at **Intuitiv Group**, for welcoming me, for the trust they placed in me
and for the time they gave to following the project and sharing their experience.

My thanks also go to the members of the jury for the honour they do me in examining
this work, and to all the teaching staff of **TEK-UP University** for the knowledge
and support they have given me throughout my studies.

Finally, I thank my family and my friends for their constant encouragement and
patience, without which this work would not have been possible.

# Abstract {.unnumbered}

Independent writers have tools to publish but few ways to be paid for quality, and
magazines that want to commission them have no objective way to judge a writer before
buying. This report presents **Inkwell.ai**, a two-sided web platform that addresses
both sides. Writers draft in a rich-text editor beside an AI assistant grounded in
their own published work and in reference documents they upload. It answers in a
panel or writes directly into the document, cites its sources by page, and accepts
spoken prompts. Every published article feeds an event-based analytics pipeline whose
audience, content and quality signals, together with AI-generated portfolio insights,
form an evaluation report that magazines use to decide. Magazines subscribe, receive
monthly credits, preview an article for 10% of its price and buy the remainder for
exclusive republication rights, every credit movement being recorded in a ledger whose
invariants are tested after each operation.

The platform was built over nine two-week Scrum sprints grouped into four releases,
with a Next.js 16 frontend, a NestJS 11 backend and worker, PostgreSQL 16 with
pgvector, Redis and BullMQ, MinIO object storage and nginx, all containerised with
Docker Compose, and with Groq and Gemini models orchestrated through the Vercel AI SDK.
The backend suite counts 796 passing tests. Measured on a labelled set, retrieval
returns a relevant passage in its top five for 89% of questions, hybrid search keeps
every relevant article in its top ten even for paraphrased queries that defeat keyword
search, and the publish-time moderation classifier reaches a precision of 0.93 and a
recall of 1.00.

**Keywords:** writing marketplace, AI-assisted writing, retrieval-augmented generation,
hybrid search, pgvector, analytics, article licensing, Scrum, NestJS, Next.js.

<!-- LISTS -->

# List of acronyms {.unnumbered}

| Acronym | Meaning |
|:----------|:----------------------------------------------------------|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| CI/CD | Continuous Integration / Continuous Deployment |
| CLS | Cumulative Layout Shift (Lighthouse metric) |
| CRUD | Create, Read, Update, Delete |
| DOCX | Office Open XML word-processing document format |
| DSDM | Dynamic Systems Development Method |
| DTO | Data Transfer Object |
| ESN | Entreprise de Services du Numérique (IT services company) |
| FR / NFR | Functional / Non-Functional Requirement |
| GHCR | GitHub Container Registry |
| HNSW | Hierarchical Navigable Small World (approximate nearest-neighbour index) |
| HTML | HyperText Markup Language |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| LCP | Largest Contentful Paint (Lighthouse metric) |
| LLM | Large Language Model |
| MoSCoW | Must, Should, Could, Won't (prioritisation) |
| MRR | Mean Reciprocal Rank |
| nDCG | normalised Discounted Cumulative Gain |
| OAuth | Open Authorization (delegated authorisation protocol) |
| OpenAPI | OpenAPI Specification (machine-readable description of a REST API) |
| ORM | Object-Relational Mapping |
| PDF | Portable Document Format |
| PFE | Projet de Fin d'Études (end-of-studies project) |
| RAG | Retrieval-Augmented Generation |
| REST | Representational State Transfer |
| RRF | Reciprocal Rank Fusion |
| S3 | Simple Storage Service (object storage protocol) |
| SQL | Structured Query Language |
| SSE | Server-Sent Events |
| TLS | Transport Layer Security |
| TTS | Text-to-Speech |
| UI | User Interface |
| UML | Unified Modeling Language |
| US | User Story |
| WCAG | Web Content Accessibility Guidelines |
