"""
Unified Intelligence Analyzer combining all intelligence engines.
"""

from datetime import UTC, datetime
from src.intelligence.classifier import FreelanceClassifier
from src.intelligence.client_enricher import ClientEnricher
from src.intelligence.pitch_strategist import PitchStrategist
from src.intelligence.requirement_extractor import RequirementExtractor
from src.intelligence.scorer import OpportunityScorer
from src.schemas.schemas import (
    ClassificationRequest,
    ClientEnrichmentRequest,
    DeepAnalysisRequest,
    DeepAnalysisResponse,
    OpportunityScoreRequest,
    PitchStrategyRequest,
    RequirementAnalysisRequest,
)


class IntelligenceAnalyzer:
    """Unified cognitive intelligence pipeline for client opportunities."""

    def __init__(self) -> None:
        self.req_extractor = RequirementExtractor()
        self.enricher = ClientEnricher()
        self.classifier = FreelanceClassifier()
        self.scorer = OpportunityScorer()
        self.strategist = PitchStrategist()

    def analyze_deep(self, req: DeepAnalysisRequest) -> DeepAnalysisResponse:
        """Run complete multi-dimensional intelligence analysis."""
        # 1. Requirements
        req_res = self.req_extractor.extract(
            RequirementAnalysisRequest(
                title=req.title,
                description=req.description,
                skills=req.skills,
                budget=req.budget,
                currency=req.currency,
            )
        )

        # 2. Client & Contact Intel
        client_res = self.enricher.enrich(
            ClientEnrichmentRequest(
                title=req.title,
                description=req.description,
                source_url=req.source_url,
                source=req.source,
            )
        )

        # 3. Freelance & Client Classification
        class_res = self.classifier.classify(
            ClassificationRequest(
                title=req.title,
                description=req.description,
                source=req.source,
            )
        )

        # 4. Multi-factor Scoring
        score_res = self.scorer.score(
            OpportunityScoreRequest(
                title=req.title,
                description=req.description,
                skills=req_res.primary_technologies,
                budget=req.budget,
                currency=req.currency,
                source=req.source,
            )
        )

        # 5. Pitch Angle Strategy
        strategy_res = self.strategist.recommend(
            PitchStrategyRequest(
                title=req.title,
                description=req.description,
                skills=req_res.primary_technologies,
                budget=req.budget,
                client_type=class_res.client_type.value,
            )
        )

        return DeepAnalysisResponse(
            requirements=req_res,
            client_intel=client_res,
            classification=class_res,
            scoring=score_res,
            pitch_strategy=strategy_res,
            analyzed_at=datetime.now(UTC),
        )


GLOBAL_ANALYZER = IntelligenceAnalyzer()
