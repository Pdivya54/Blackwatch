# This node implements the Executive Reporter Agent, which compiles all gathered metrics and text into a final report.
# It packages upstream calculations, risk assessments, and mitigation plans into a unified C-suite markdown brief.

import os 
from langchain_anthropic import ChatAnthropic  
from core.config import settings, AdIntelligenceState
from dotenv import load_dotenv

load_dotenv()

def run_executive_reporter_agent(state: AdIntelligenceState):
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        temperature=settings.temperature,
        api_key=settings.anthropic_api_key
    )
    mitigation = state.get("proactive_mitigation_plan", {}).get(
        "defensive_copy", "No proactive mitigation required."
    )
    prompt = f"""Compile a comprehensive Executive Marketing Intelligence Brief using the provided data:
    - Target Entity: {state.get('brand_name')} ({state.get('ticker_symbol')})
    - Monitored Competitor Strategy: {state.get('ad_campaign_data')}
    - Strategic Risk Assessment: {state.get('threat_matrix_assessment', {}).get('exposure_verdict_analysis')}
    - PROACTIVE MITIGATION FRAMEWORK: {mitigation}
    
    Structure the report clearly in Markdown. Include high-priority strategic observations, future risk projections, and recommended defensive maneuvers for management."""
    
    res = llm.invoke(prompt)
    
    return {
        "executive_brief_markdown": res.content,
        "pipeline_audit_trail": ["Executive Reporter finalized the complete predictive briefing package."]
    }