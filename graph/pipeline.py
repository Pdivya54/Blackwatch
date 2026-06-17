# This script defines the core routing architecture and state graph orchestration using LangGraph.
# It registers all specialized agent nodes, establishes communication paths, and compiles the workflow into an executable app_graph binary.


from langgraph.graph import StateGraph, START, END
from typing import Literal
from core.config import AdIntelligenceState

from agents.supervisor import supervisor_node
from agents.ad_scout_agent import run_ad_scout_agent
from agents.risk_vulnerability_agent import run_risk_vulnerability_agent
from agents.strategy_matrix_agent import run_strategy_matrix_agent
from agents.proactive_mitigation_agent import run_proactive_mitigation_agent
from agents.executive_reporter_agent import run_executive_reporter_agent

def determine_route(state: AdIntelligenceState) -> Literal[
    "ad_scout_agent", 
    "risk_vulnerability_agent", 
    "strategy_matrix_agent", 
    "proactive_mitigation_agent", 
    "executive_reporter_agent", 
    "__end__"
]:
    target = state.get("next_agent", "__end__")
    return END if target == "__end__" else target

workflow = StateGraph(AdIntelligenceState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("ad_scout_agent", run_ad_scout_agent)
workflow.add_node("risk_vulnerability_agent", run_risk_vulnerability_agent)
workflow.add_node("strategy_matrix_agent", run_strategy_matrix_agent)
workflow.add_node("proactive_mitigation_agent", run_proactive_mitigation_agent)
workflow.add_node("executive_reporter_agent", run_executive_reporter_agent)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    determine_route,
    {
        "ad_scout_agent": "ad_scout_agent",
        "risk_vulnerability_agent": "risk_vulnerability_agent",
        "strategy_matrix_agent": "strategy_matrix_agent",
        "proactive_mitigation_agent": "proactive_mitigation_agent",
        "executive_reporter_agent": "executive_reporter_agent",
        "__end__": END
    }
)

workflow.add_edge("ad_scout_agent", "supervisor")
workflow.add_edge("risk_vulnerability_agent", "supervisor")
workflow.add_edge("strategy_matrix_agent", "supervisor")
workflow.add_edge("proactive_mitigation_agent", "supervisor")
workflow.add_edge("executive_reporter_agent", "supervisor")

app_graph = workflow.compile()