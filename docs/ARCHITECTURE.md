# Architecture & Design Reference
## Client Intelligence Service (`CLIENT-INTELLIGENCE-SVC`)

---

## 1. Role & System Responsibility
The **Client Intelligence Service (`CLIENT-INTELLIGENCE-SVC`)** (Port 8002) is the cognitive analysis engine of the platform. It takes raw text job postings, freelance gigs, or consulting inquiries and produces deep, structured, evidence-backed intelligence:

1. **Requirement Extraction**: Parses languages, frameworks, libraries, explicit deliverables, complexity tiers, and budget viability.
2. **Client & Contact Enrichment**: Detects client entity names, websites, domains, decision-maker identity, emails, and calculates explicit confidence scores ($0.0 - 1.0$).
3. **Freelance & Client Classification**: Classifies whether a lead is a **Direct Client** (founder, hiring manager) or an **Intermediary / Agency** (broker, recruiter), and identifies engagement type (Fixed Price, Hourly, Fractional Retainer).
4. **Multi-Factor Opportunity Scoring**: Computes a 0-100 composite ranking based on skill match, budget attractiveness, client quality, and win probability.
5. **Pitch Angle Strategist**: Recommends the optimal conversion angle (`technical_expert`, `speed_delivery`, `fractional_advisor`, `case_study_proof`).

---

## 2. Intelligence Pipeline Architecture

```
                    ┌────────────────────────┐
                    │     Raw Opportunity    │
                    │  (Title + Description) │
                    └───────────┬────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  Requirement  │       │  Client & CRM │       │  Freelance &  │
│   Extractor   │       │   Enricher    │       │  Client Class │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │ Multi-Factor Scorer   │
                    │ & Win Probability     │
                    └───────────┬───────────┘
                                ▼
                    ┌───────────────────────┐
                    │ Pitch Angle Strategist│
                    └───────────┬───────────┘
                                ▼
                    ┌───────────────────────┐
                    │ Enriched Intelligence │
                    │ (Structured Payload)  │
                    └───────────────────────┘
```
