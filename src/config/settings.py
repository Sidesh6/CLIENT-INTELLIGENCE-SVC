from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for Client Intelligence Service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="development")
    app_debug: bool = Field(default=False)
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8002)

    database_url: str = Field(default="sqlite:///./data/intelligence.db")

    # Scoring algorithm weights
    weight_skill_match: float = 0.35
    weight_budget: float = 0.25
    weight_client_quality: float = 0.20
    weight_competition: float = 0.10
    weight_freshness: float = 0.10

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent.parent

    @property
    def data_dir(self) -> Path:
        d = self.base_dir / "data"
        d.mkdir(parents=True, exist_ok=True)
        return d


settings = Settings()
