# This node implements the Strategy Matrix Agent, combining mathematical forecasting with LLM evaluation.
# It feeds raw market metrics into our asset decay tools and uses an LLM to generate a sharp corporate risk assessment and a categorical threat badge.

import os
from langchain_anthropic import ChatAnthropic
from core.config import settings, AdIntelligenceState
from tools.intelligence_tools import project_future_risk_curve
from dotenv import load_dotenv

load_dotenv()

def run_strategy_matrix_agent(state: AdIntelligenceState):

    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",  
        temperature=settings.temperature,
        api_key=settings.anthropic_api_key
    )

    current_price = state.get("equity_risk_metrics", {}).get("last_closing_value", 100.0)
    volatility = state.get("equity_risk_metrics", {}).get("baseline_volatility_pct", 15.0)
    sim_mod = state.get("simulation_modifiers", {"backlash_index": 0.4})
    backlash_mult = sim_mod.get("backlash_index", 0.4) * 10.0

    future_forecast = project_future_risk_curve(current_price, volatility, backlash_mult)

    prompt = f"""You are a Market Strategy Consultant.
    Review the following technical indicators and competitive intelligence:
    - Competitor Market Footprint: {state.get('ad_campaign_data')}
    - Baseline Market Volatility: {state.get('equity_risk_metrics')}
    - 60-Day Projected Risk Horizon: {future_forecast}
    
    Provide a professional assessment of market risk. 
    1. Summarize key competitive vulnerabilities.
    2. Assess asset volatility risks.
    3. Conclude with a risk classification: [STABLE RISK], [ELEVATED EXPOSURE], or [CRITICAL THREAT PROTOCOL]."""
    
    res = llm.invoke(prompt)
    content = res.content

    threat_badge = "ELEVATED EXPOSURE"
    if "CRITICAL" in content.upper():
        threat_badge = "CRITICAL THREAT PROTOCOL"
    elif "STABLE" in content.upper():
        threat_badge = "STABLE RISK"

    return {
        "threat_matrix_assessment": {
            "exposure_verdict_analysis": content,
            "derived_threat_level": threat_badge,
            "predictive_forecast_data": future_forecast,
        },
        "pipeline_audit_trail": [
            "Strategy Matrix operative computed mathematical 60-day risk projections."
        ],
    }