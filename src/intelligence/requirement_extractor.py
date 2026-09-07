"""
Requirement extraction engine for parsing technologies, deliverables, and complexity.
"""

import re
from typing import Optional
from src.schemas.schemas import RequirementAnalysisRequest, RequirementAnalysisResponse

TECH_TAXONOMY = {
    "python": ["python", "python3", "py", "django", "flask", "fastapi", "pandas", "numpy"],
    "fastapi": ["fastapi", "asgi", "starlette", "pydantic"],
    "postgresql": ["postgres", "postgresql", "psql", "pgvector", "pg"],
    "rag": ["rag", "retrieval augmented generation", "vector search", "embeddings", "pinecone", "chromadb", "weaviate", "qdrant"],
    "llm": ["llm", "large language model", "openai", "gpt-4", "claude", "gemini", "langchain", "llamaindex", "ollama"],
    "docker": ["docker", "container", "docker-compose", "k8s", "kubernetes"],
    "react": ["react", "reactjs", "next.js", "nextjs", "typescript"],
    "angular": ["angular", "angularjs", "typescript", "rxjs"],
    "sql": ["sql", "mysql", "sqlite", "database", "sqlalchemy"],
    "aws": ["aws", "s3", "lambda", "ec2", "cloud"],
}

DELIVERABLE_PATTERNS = [
    (r"\b(rest\s*api|endpoint|microservice|backend)\b", "REST API / Backend Service"),
    (r"\b(scraper|scraping|crawler|extractor)\b", "Web Scraper / Data Extractor"),
    (r"\b(pipeline|etl|ingestion|data flow)\b", "Data Processing Pipeline"),
    (r"\b(vector\s*search|rag|semantic\s*search)\b", "RAG Vector Search Engine"),
    (r"\b(dashboard|ui|frontend|portal)\b", "Frontend Dashboard / Portal"),
    (r"\b(database|schema|migration|models)\b", "Database Architecture & Migrations"),
    (r"\b(bot|agent|automation)\b", "AI Agent / Automation Bot"),
]


class RequirementExtractor:
    """Extracts structured requirements and complexity from project text."""

    def extract(self, req: RequirementAnalysisRequest) -> RequirementAnalysisResponse:
        text = f"{req.title} {req.description}".lower()
        extracted_techs: set[str] = set()

        # 1. Match taxonomy
        for canonical, aliases in TECH_TAXONOMY.items():
            for alias in aliases:
                if re.search(rf"\b{re.escape(alias)}\b", text):
                    extracted_techs.add(canonical.capitalize())
                    break

        # Include explicitly passed skills
        for s in req.skills:
            if s and s.strip():
                extracted_techs.add(s.strip())

        # 2. Extract deliverables
        deliverables: list[str] = []
        for pattern, label in DELIVERABLE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                if label not in deliverables:
                    deliverables.append(label)

        if not deliverables:
            deliverables.append("Custom Software Development")

        # 3. Complexity & Urgency estimation
        word_count = len(req.description.split())
        tech_count = len(extracted_techs)

        if tech_count >= 5 or word_count > 250 or (req.budget and req.budget >= 5000):
            complexity = "high"
        elif tech_count >= 3 or word_count > 100 or (req.budget and req.budget >= 1500):
            complexity = "medium"
        else:
            complexity = "low"

        # Urgency
        if re.search(r"\b(urgent|asap|immediately|today|quick turnaround)\b", text):
            urgency = "high"
        elif re.search(r"\b(this week|soon|flexible)\b", text):
            urgency = "medium"
        else:
            urgency = "flexible"

        # Budget adequacy
        budget = req.budget
        if budget:
            if budget >= 4000:
                adequacy = "premium"
            elif budget >= 1500:
                adequacy = "high"
            elif budget >= 500:
                adequacy = "moderate"
            else:
                adequacy = "low"
        else:
            adequacy = "moderate"

        project_goal = req.title.strip()
        if len(project_goal) < 10 and deliverables:
            project_goal = f"Deliver {deliverables[0]} for client project"

        return RequirementAnalysisResponse(
            primary_technologies=sorted(list(extracted_techs)),
            deliverables=deliverables,
            complexity_level=complexity,
            project_goal=project_goal,
            urgency=urgency,
            extracted_budget=budget,
            budget_adequacy=adequacy,
        )
