# This node implements the Proactive Mitigation Agent, which acts as a generative defensive asset builder.
# It evaluates downstream asset decay forecasts and leverages an LLM to auto-generate defensive PR copy and narrative pivot frameworks.

import os  
from langchain_anthropic import ChatAnthropic  
from core.config import settings, AdIntelligenceState
from dotenv import load_dotenv

load_dotenv()

def run_proactive_mitigation_agent(state: AdIntelligenceState):
    # agents/strategy_matrix_agent.py

    llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",  
    temperature=settings.temperature,
    api_key=settings.anthropic_api_key
)
    forecast = state.get("threat_matrix_assessment", {}).get("predictive_forecast_data", [])
    
    prompt = f"""You are a Strategic Corporate Communications Advisor. 
    The Strategy Matrix has identified a potential future market volatility trajectory based on this data: {forecast}
    
    Your goal is to draft professional, transparent, and proactive corporate communication strategies to maintain stakeholder confidence and brand stability.
    Please provide:
    1. A transparent brand positioning statement that emphasizes long-term value.
    2. A framework for proactive narrative management that clarifies brand objectives to the market.
    Focus on clarity, market resilience, and building long-term trust."""
    
    res = llm.invoke(prompt)
    
    return {
        "proactive_mitigation_plan": {"defensive_copy": res.content},
        "pipeline_audit_trail": ["Proactive Mitigation Agent auto-generated future defensive action assets."]
    }