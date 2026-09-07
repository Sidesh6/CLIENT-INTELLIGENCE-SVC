"""
Pitch angle and strategic positioning engine.
"""

from src.schemas.schemas import PitchAngle, PitchStrategyRequest, PitchStrategyResponse


class PitchStrategist:
    """Selects the highest converting outreach angle and hook."""

    def recommend(self, req: PitchStrategyRequest) -> PitchStrategyResponse:
        text = f"{req.title} {req.description}".lower()

        if "urgent" in text or "asap" in text or "quick" in text:
            angle = PitchAngle.SPEED_DELIVERY
            hook = "I saw you're looking for an immediate turnaround on this deliverable—I can deploy a working initial build within 48 hours."
            selling_points = [
                "Immediate availability for sprint kickoff",
                "Proven track record of high-velocity microservice delivery",
                "Clear milestone-based delivery schedule",
            ]
            cta = "Are you available for a quick 10-minute sync today to review the initial technical scope?"

        elif req.budget and req.budget >= 5000:
            angle = PitchAngle.FRACTIONAL_ADVISOR
            hook = f"Your architectural requirements for '{req.title}' align directly with scalable enterprise systems I've designed."
            selling_points = [
                "End-to-end architecture and system design",
                "Senior technical guidance and schema optimization",
                "Long-term maintainability and automated test coverage",
            ]
            cta = "Would you be open to reviewing an architectural outline this week?"

        elif "rag" in text or "llm" in text or "fastapi" in text or "python" in text:
            angle = PitchAngle.CASE_STUDY_PROOF
            hook = "I recently engineered a sub-200ms document processing and search pipeline using the exact same stack you specified."
            selling_points = [
                "Demonstrated benchmarked performance with pgvector & FastAPI",
                "Clean production-grade repository with comprehensive tests",
                "Zero-fluff technical execution focused on measurable latency metrics",
            ]
            cta = "Open to a brief chat Tuesday to discuss how I can implement a similar architecture for your project?"

        else:
            angle = PitchAngle.TECHNICAL_EXPERT
            hook = f"I specialize in building robust backend services and APIs matching your stated requirements for {req.title}."
            selling_points = [
                "Deep specialization in Python and modern API frameworks",
                "Clean code architecture with comprehensive test suites",
                "Transparent async communication and daily milestone updates",
            ]
            cta = "Are you open to a brief technical discussion this week?"

        return PitchStrategyResponse(
            recommended_angle=angle,
            hook_sentence=hook,
            key_selling_points=selling_points,
            call_to_action=cta,
        )
