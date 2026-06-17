# This node acts as the central state-driven router and orchestrator for the LangGraph workflow.
# It evaluates the current global state keys dynamically to determine and dispatch the next optimal agent node or terminate the execution.


from typing import Dict, Any
from core.config import AdIntelligenceState

def supervisor_node(state: AdIntelligenceState) -> Dict[str, Any]:
    has_ad_data = bool(state.get("ad_campaign_data"))
    has_risk_data = bool(state.get("equity_risk_metrics"))
    has_matrix_data = bool(state.get("threat_matrix_assessment"))
    
    derived_threat = state.get("threat_matrix_assessment", {}).get("derived_threat_level", "")
    requires_mitigation = "CRITICAL" in derived_threat or "ELEVATED" in derived_threat
    has_mitigation_plan = bool(state.get("proactive_mitigation_plan"))
    
    has_brief = bool(state.get("executive_brief_markdown"))

    if not has_ad_data:
        next_agent = "ad_scout_agent"
    elif not has_risk_data:
        next_agent = "risk_vulnerability_agent"
    elif not has_matrix_data:
        next_agent = "strategy_matrix_agent"
    elif requires_mitigation and not has_mitigation_plan:
        next_agent = "proactive_mitigation_agent"
    elif not has_brief:
        next_agent = "executive_reporter_agent"
    else:
        next_agent = "__end__"

    return {
        "next_agent": next_agent,
        "pipeline_audit_trail": [f"SUPERVISOR -> Dispatched to: {next_agent}"]
    }