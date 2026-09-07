"""
CLI Interface for Client Intelligence Service.
"""

import json
import click
import uvicorn
from src.config.settings import settings
from src.intelligence.analyzer import GLOBAL_ANALYZER
from src.schemas.schemas import DeepAnalysisRequest


@click.group()
def cli() -> None:
    """Client Intelligence Service CLI."""
    pass


@cli.command("run-server")
@click.option("--host", default=None, help="Host to bind.")
@click.option("--port", default=None, type=int, help="Port to bind.")
@click.option("--reload", is_flag=True, default=False, help="Auto-reload.")
def cmd_run_server(host: str | None, port: int | None, reload: bool) -> None:
    """Start Client Intelligence REST API."""
    bind_host = host or settings.app_host
    bind_port = port or settings.app_port
    click.secho(f"[*] Starting Client Intelligence Service on http://{bind_host}:{bind_port}", fg="green")
    click.secho(f"[*] Swagger Docs: http://{bind_host}:{bind_port}/docs", fg="cyan")
    uvicorn.run("src.api.main:app", host=bind_host, port=bind_port, reload=reload)


@cli.command("analyze")
@click.option("--title", required=True, help="Project title.")
@click.option("--desc", required=True, help="Project description.")
@click.option("--budget", default=None, type=float, help="Budget amount.")
@click.option("--skills", default="", help="Comma-separated skills.")
def cmd_analyze(title: str, desc: str, budget: float | None, skills: str) -> None:
    """Analyze a project opportunity in the terminal."""
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    req = DeepAnalysisRequest(
        title=title,
        description=desc,
        budget=budget,
        skills=skill_list,
    )
    result = GLOBAL_ANALYZER.analyze_deep(req)

    click.secho(f"\n================ Opportunity Intelligence ================", fg="cyan", bold=True)
    click.secho(f"Title: {title}", fg="white", bold=True)
    click.secho(f"Verdict: [{result.scoring.qualification_verdict}] | Score: {result.scoring.score.overall_score}/100", fg="yellow")
    click.secho(f"Win Probability: {result.scoring.score.win_probability * 100:.0f}%", fg="green")

    click.secho("\n[+] Extracted Requirements:", fg="cyan")
    click.secho(f"  • Technologies: {', '.join(result.requirements.primary_technologies) or 'None'}")
    click.secho(f"  • Deliverables: {', '.join(result.requirements.deliverables)}")
    click.secho(f"  • Complexity: {result.requirements.complexity_level.upper()} | Urgency: {result.requirements.urgency.upper()}")

    click.secho("\n[+] Client Intelligence:", fg="cyan")
    contact = result.client_intel.contact
    click.secho(f"  • Contact Name: {contact.name or 'N/A'}")
    click.secho(f"  • Company: {contact.company or 'N/A'}")
    click.secho(f"  • Email: {contact.email or 'N/A'}")
    click.secho(f"  • Client Type: {result.classification.client_type.value.upper()} (Direct: {result.classification.is_direct_client})")

    click.secho("\n[+] Recommended Pitch Strategy:", fg="cyan")
    click.secho(f"  • Angle: {result.pitch_strategy.recommended_angle.value.upper()}")
    click.secho(f"  • Hook: \"{result.pitch_strategy.hook_sentence}\"")
    click.echo()


if __name__ == "__main__":
    cli()
