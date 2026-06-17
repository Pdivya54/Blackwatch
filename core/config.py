# This file handles global environment configurations using Pydantic Settings and defines the unified state schema for LangGraph.
# It ensures environment variables are validated on startup and provides a strictly typed dictionary template for multi-agent data tracking.


import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing_extensions import TypedDict
from typing import Dict, Any, List

class Settings(BaseSettings):
    anthropic_api_key: str = Field(alias="ANTHROPIC_API_KEY")
    model_name: str = "claude-haiku-4-5-20251001"
    temperature: float = 0.15
    host: str = "127.0.0.1"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

class AdIntelligenceState(TypedDict):
    brand_name: str
    ticker_symbol: str
    simulation_modifiers: Dict[str, Any]
    ad_campaign_data: Dict[str, Any]
    equity_risk_metrics: Dict[str, Any]
    threat_matrix_assessment: Dict[str, Any]
    proactive_mitigation_plan: Dict[str, Any]
    executive_brief_markdown: str
    next_agent: str
    pipeline_audit_trail: List[str]