---
title: "Inkwell.ai — An AI-Powered Writing Marketplace Connecting Independent Writers and Magazine Publishers"
subtitle: "End-of-Studies Project Report (Projet de Fin d'Études)"
author: "Oussama Bejaoui"
date: "Academic year 2025–2026"
lang: en-GB
---

::: {.titlepage}

**TEK-UP University**

**GLSI — Software Engineering and Information Systems**

&nbsp;

# End-of-Studies Project Report {.unnumbered .unlisted}

Submitted in partial fulfilment of the requirements for the degree of
**National Engineering Diploma in Computer Science (GLSI)**

&nbsp;

## Inkwell.ai {.unnumbered .unlisted}

### An AI-powered writing marketplace connecting independent writers and magazine publishers {.unnumbered .unlisted}

&nbsp;

Carried out by: **Oussama Bejaoui**

Academic supervisor: **Mr. Bilel Zemzem**

Professional supervisor: **Mr. Ramzy Chridi**

Host organisation: **Intuitiv Group**

&nbsp;

Project period: **1 February 2026 – 31 July 2026**

Academic year **2025–2026**

:::

\newpage

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

\newpage

# Abstract {.unnumbered}

Independent writers have tools to publish but few ways to be paid for quality, and
magazines that want to commission them have no objective way to judge a writer before
buying. This report presents **Inkwell.ai**, a two-sided web platform that addresses
both sides. Writers draft in a rich-text editor beside an AI assistant grounded in
their own published work and in reference documents they upload; it answers in a
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
The backend suite counts 792 passing tests in 51 suites.

**Keywords:** writing marketplace, AI-assisted writing, retrieval-augmented generation,
pgvector, analytics, article licensing, Scrum, NestJS, Next.js.

\newpage

# Résumé {.unnumbered}

Les rédacteurs indépendants disposent d'outils pour publier, mais de peu de moyens
d'être rémunérés pour la qualité de leur travail, et les magazines qui souhaitent leur
confier des articles n'ont aucun moyen objectif d'évaluer un rédacteur avant d'acheter.
Ce rapport présente **Inkwell.ai**, une plateforme web biface qui répond aux deux
besoins. Les rédacteurs écrivent dans un éditeur de texte enrichi, aux côtés d'un
assistant d'intelligence artificielle ancré dans leurs propres articles publiés et dans
les documents de référence qu'ils déposent ; l'assistant répond dans un panneau ou écrit
directement dans le document, cite ses sources à la page près et accepte des consignes
dictées à la voix. Chaque article publié alimente une chaîne d'analyse fondée sur des
événements, dont les indicateurs d'audience, de contenu et de qualité, complétés par une
synthèse générée par l'IA, constituent un rapport d'évaluation sur lequel les magazines
s'appuient pour décider. Les magazines s'abonnent, reçoivent des crédits mensuels,
débloquent un aperçu pour 10 % du prix et achètent le reste pour obtenir des droits de
republication exclusifs ; chaque mouvement de crédits est inscrit dans un grand livre
dont les invariants sont vérifiés après chaque opération.

La plateforme a été réalisée en neuf sprints Scrum de deux semaines, regroupés en
quatre releases, avec un frontend Next.js 16, un backend et un worker NestJS 11,
PostgreSQL 16 avec pgvector, Redis et BullMQ, le stockage objet MinIO et nginx, le tout
conteneurisé avec Docker Compose, les modèles Groq et Gemini étant orchestrés par le
Vercel AI SDK. La suite de tests du backend compte 792 tests réussis répartis en 51
suites.

**Mots-clés :** place de marché d'écriture, rédaction assistée par l'IA, génération
augmentée par la recherche, pgvector, analytique, licence d'articles, Scrum, NestJS,
Next.js.

\newpage

# List of acronyms {.unnumbered}

| Acronym | Meaning |
|---|---|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| CI/CD | Continuous Integration / Continuous Deployment |
| CRUD | Create, Read, Update, Delete |
| DTO | Data Transfer Object |
| FR / NFR | Functional / Non-Functional Requirement |
| GHCR | GitHub Container Registry |
| HNSW | Hierarchical Navigable Small World (approximate nearest-neighbour index) |
| JWT | JSON Web Token |
| LLM | Large Language Model |
| MoSCoW | Must, Should, Could, Won't (prioritisation) |
| ORM | Object-Relational Mapping |
| PFE | Projet de Fin d'Études (end-of-studies project) |
| RAG | Retrieval-Augmented Generation |
| RRF | Reciprocal Rank Fusion |
| S3 | Simple Storage Service (object storage protocol) |
| SSE | Server-Sent Events |
| TLS | Transport Layer Security |
| TTS | Text-to-Speech |
| UML | Unified Modeling Language |
| US | User Story |

\newpage
