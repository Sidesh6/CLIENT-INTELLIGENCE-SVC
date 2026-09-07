"""
FastAPI application for Client Intelligence Service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import analyze_router, health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Client Intelligence Service API",
        description="Lead enrichment, requirement extraction, multi-factor scoring, and classification service.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(analyze_router)

    @app.get("/", tags=["Root"])
    def root() -> dict[str, str]:
        return {
            "service": "Client Intelligence Service",
            "version": "0.1.0",
            "docs": "/docs",
            "health": "/health",
        }

    return app


app = create_app()
