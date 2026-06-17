# In agents/ad_scout_agent.py
from core.config import AdIntelligenceState
from tools.intelligence_tools import get_brand_market_data 

def run_ad_scout_agent(state: AdIntelligenceState):
    brand = state.get("brand_name", "Nike")
    
    campaign_metrics = get_brand_market_data(brand)
    
    return {
        "ad_campaign_data": campaign_metrics,
        "pipeline_audit_trail": [f"Scouted marketing data for {brand}."]
    }