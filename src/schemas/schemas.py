"""
Pydantic schemas for Client Intelligence API and domain engines.
"""

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Optional
from pydantic import BaseModel, Field


class ClientType(StrEnum):
    DIRECT_CLIENT = "direct_client"
    AGENCY = "agency"
    RECRUITER = "recruiter"
    UNKNOWN = "unknown"


class EngagementType(StrEnum):
    FIXED_PRICE = "fixed_price"
    HOURLY = "hourly"
    RETAINER = "retainer"
    FULL_TIME = "full_time"
    UNKNOWN = "unknown"


class PitchAngle(StrEnum):
    TECHNICAL_EXPERT = "technical_expert"
    SPEED_DELIVERY = "speed_delivery"
    FRACTIONAL_ADVISOR = "fractional_advisor"
    CASE_STUDY_PROOF = "case_study_proof"


class ContactDetail(BaseModel):
    """Extracted contact information with source evidence."""
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    domain: Optional[str] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    source_evidence: list[str] = Field(default_factory=list)


class RequirementAnalysisRequest(BaseModel):
    title: str
    description: str
    skills: list[str] = Field(default_factory=list)
    budget: Optional[float] = None
    currency: str = "USD"


class RequirementAnalysisResponse(BaseModel):
    primary_technologies: list[str]
    deliverables: list[str]
    complexity_level: str = "medium"  # low, medium, high, enterprise
    project_goal: str
    urgency: str = "medium"  # low, medium, high
    extracted_budget: Optional[float] = None
    budget_adequacy: str = "moderate"  # low, moderate, high, premium


class ClientEnrichmentRequest(BaseModel):
    title: str
    description: str
    source_url: Optional[str] = None
    source: Optional[str] = None


class ClientEnrichmentResponse(BaseModel):
    contact: ContactDetail
    client_type: ClientType
    engagement_type: EngagementType
    industry: Optional[str] = None
    company_size_estimate: Optional[str] = None
    risk_flags: list[str] = Field(default_factory=list)


class ClassificationRequest(BaseModel):
    title: str
    description: str
    source: Optional[str] = None


class ClassificationResponse(BaseModel):
    is_direct_client: bool
    client_type: ClientType
    engagement_type: EngagementType
    confidence: float
    rationale: str


class ScoreBreakdown(BaseModel):
    overall_score: float = Field(ge=0.0, le=100.0)
    skill_match_score: float = Field(ge=0.0, le=100.0)
    budget_score: float = Field(ge=0.0, le=100.0)
    client_score: float = Field(ge=0.0, le=100.0)
    competition_score: float = Field(ge=0.0, le=100.0)
    freshness_score: float = Field(ge=0.0, le=100.0)
    win_probability: float = Field(ge=0.0, le=1.0)
    explanation: str


class OpportunityScoreRequest(BaseModel):
    title: str
    description: str
    skills: list[str] = Field(default_factory=list)
    budget: Optional[float] = None
    currency: str = "USD"
    source: Optional[str] = None
    user_skills: list[str] = Field(
        default_factory=lambda: ["Python", "FastAPI", "PostgreSQL", "RAG", "LLM", "Docker", "SQLAlchemy", "React", "Angular"]
    )


class OpportunityScoreResponse(BaseModel):
    score: ScoreBreakdown
    qualification_verdict: str  # QUALIFIED, HIGH_PRIORITY, LOW_PRIORITY, DISQUALIFIED


class PitchStrategyRequest(BaseModel):
    title: str
    description: str
    skills: list[str] = Field(default_factory=list)
    budget: Optional[float] = None
    client_type: Optional[str] = None


class PitchStrategyResponse(BaseModel):
    recommended_angle: PitchAngle
    hook_sentence: str
    key_selling_points: list[str]
    call_to_action: str


class DeepAnalysisRequest(BaseModel):
    """Unified full analysis request."""
    title: str
    description: str
    source: str = "Web"
    source_url: Optional[str] = None
    budget: Optional[float] = None
    currency: str = "USD"
    skills: list[str] = Field(default_factory=list)


class DeepAnalysisResponse(BaseModel):
    """Unified full analysis output for an opportunity."""
    requirements: RequirementAnalysisResponse
    client_intel: ClientEnrichmentResponse
    classification: ClassificationResponse
    scoring: OpportunityScoreResponse
    pitch_strategy: PitchStrategyResponse
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
