"""
REST API endpoints for Client Intelligence Service.
"""

from fastapi import APIRouter
from src.intelligence.analyzer import GLOBAL_ANALYZER
from src.intelligence.classifier import FreelanceClassifier
from src.intelligence.client_enricher import ClientEnricher
from src.intelligence.pitch_strategist import PitchStrategist
from src.intelligence.requirement_extractor import RequirementExtractor
from src.intelligence.scorer import OpportunityScorer
from src.schemas.schemas import (
    ClassificationRequest,
    ClassificationResponse,
    ClientEnrichmentRequest,
    ClientEnrichmentResponse,
    DeepAnalysisRequest,
    DeepAnalysisResponse,
    OpportunityScoreRequest,
    OpportunityScoreResponse,
    PitchStrategyRequest,
    PitchStrategyResponse,
    RequirementAnalysisRequest,
    RequirementAnalysisResponse,
)

router = APIRouter(prefix="/api/v1", tags=["Intelligence"])

_extractor = RequirementExtractor()
_enricher = ClientEnricher()
_classifier = FreelanceClassifier()
_scorer = OpportunityScorer()
_strategist = PitchStrategist()


@router.post("/analyze/project", response_model=DeepAnalysisResponse)
def analyze_deep(payload: DeepAnalysisRequest) -> DeepAnalysisResponse:
    """Run full cognitive analysis across all intelligence dimensions."""
    return GLOBAL_ANALYZER.analyze_deep(payload)


@router.post("/extract/requirements", response_model=RequirementAnalysisResponse)
def extract_requirements(payload: RequirementAnalysisRequest) -> RequirementAnalysisResponse:
    """Extract technical stack, deliverables, complexity, and urgency."""
    return _extractor.extract(payload)


@router.post("/enrich/client", response_model=ClientEnrichmentResponse)
def enrich_client(payload: ClientEnrichmentRequest) -> ClientEnrichmentResponse:
    """Enrich client contacts, domains, and business type."""
    return _enricher.enrich(payload)


@router.post("/classify", response_model=ClassificationResponse)
def classify_client(payload: ClassificationRequest) -> ClassificationResponse:
    """Classify direct client vs recruiter/broker and engagement type."""
    return _classifier.classify(payload)


@router.post("/score", response_model=OpportunityScoreResponse)
def score_opportunity(payload: OpportunityScoreRequest) -> OpportunityScoreResponse:
    """Calculate transparent multi-factor ranking and win probability."""
    return _scorer.score(payload)


@router.post("/strategy", response_model=PitchStrategyResponse)
def recommend_pitch_strategy(payload: PitchStrategyRequest) -> PitchStrategyResponse:
    """Recommend best outreach pitch angle and hook."""
    return _strategist.recommend(payload)
