"""
Multi-factor opportunity scoring and win probability engine.
"""

from src.config.settings import settings
from src.schemas.schemas import OpportunityScoreRequest, OpportunityScoreResponse, ScoreBreakdown


class OpportunityScorer:
    """Computes transparent, multi-dimensional scores for incoming opportunities."""

    def score(self, req: OpportunityScoreRequest) -> OpportunityScoreResponse:
        title_desc = f"{req.title} {req.description}".lower()
        user_skills_lower = [s.lower() for s in req.user_skills]

        # 1. Skill Match Score (0 - 100)
        matched = 0
        total_req = max(1, len(req.skills))
        for skill in req.skills:
            if skill.lower() in user_skills_lower or skill.lower() in title_desc:
                matched += 1

        # Also check direct mentions in text
        for us in user_skills_lower:
            if us in title_desc:
                matched += 0.5

        skill_match_score = min(100.0, max(20.0, (matched / total_req) * 85.0 + 15.0))

        # 2. Budget Score (0 - 100)
        if req.budget is not None:
            if req.budget >= 5000:
                budget_score = 95.0
            elif req.budget >= 2500:
                budget_score = 85.0
            elif req.budget >= 1000:
                budget_score = 70.0
            elif req.budget >= 500:
                budget_score = 55.0
            else:
                budget_score = 40.0
        else:
            budget_score = 65.0  # Default estimate

        # 3. Client Score (0 - 100)
        client_score = 70.0
        if req.source in ("Hacker News", "Direct Email", "Founder Inquiries"):
            client_score += 20.0
        if "@" in req.description:
            client_score += 10.0
        client_score = min(100.0, client_score)

        # 4. Competition Score (0 - 100)
        if req.source in ("Upwork", "Freelancer"):
            competition_score = 45.0
        else:
            competition_score = 80.0

        # 5. Freshness Score (0 - 100)
        freshness_score = 90.0

        # Weighted Overall Score
        overall = (
            skill_match_score * settings.weight_skill_match
            + budget_score * settings.weight_budget
            + client_score * settings.weight_client_quality
            + competition_score * settings.weight_competition
            + freshness_score * settings.weight_freshness
        )
        overall = round(min(100.0, max(0.0, overall)), 1)

        # Win probability estimation
        win_prob = round(min(0.95, max(0.1, (overall / 100.0) * 0.85 + 0.1)), 2)

        # Verdict
        if overall >= 85.0:
            verdict = "HIGH_PRIORITY"
            explanation = "Exceptional opportunity: high skill overlap with strong budget and verified client signals."
        elif overall >= 75.0:
            verdict = "QUALIFIED"
            explanation = "Qualified lead: strong technical alignment suitable for tailored proposal."
        elif overall >= 50.0:
            verdict = "LOW_PRIORITY"
            explanation = "Moderate alignment: consider outreach only if capacity allows."
        else:
            verdict = "DISQUALIFIED"
            explanation = "Low fit: budget or technical requirements deviate from primary target competencies."

        breakdown = ScoreBreakdown(
            overall_score=overall,
            skill_match_score=round(skill_match_score, 1),
            budget_score=round(budget_score, 1),
            client_score=round(client_score, 1),
            competition_score=round(competition_score, 1),
            freshness_score=round(freshness_score, 1),
            win_probability=win_prob,
            explanation=explanation,
        )

        return OpportunityScoreResponse(
            score=breakdown,
            qualification_verdict=verdict,
        )
