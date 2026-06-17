# This script sets up a FastAPI server that exposes a REST API endpoint for the application.
# It receives user inputs from the dashboard, formats them into the initial LangGraph state, and triggers the multi-agent pipeline.


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.pipeline import app_graph
from core.config import settings
import uvicorn
import traceback 
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="PROJECT BLACKWATCH: FUTURE-LOOKING INTERCEPT INTERFACE")

class InterceptPayload(BaseModel):
    brand_name: str
    ticker_symbol: str
    simulation_modifiers: dict

@app.post("/api/v1/intercept")
async def handle_intercept(payload: InterceptPayload):
    try:
        initial_runtime_state = {
            "ticker_symbol": payload.ticker_symbol.upper().strip(),
            "brand_name": payload.brand_name.upper().strip(),
            "simulation_modifiers": payload.simulation_modifiers,
            "ad_campaign_data": {},
            "equity_risk_metrics": {},
            "threat_matrix_assessment": {},
            "proactive_mitigation_plan": {},
            "executive_brief_markdown": "",
            "next_agent": "",
            "pipeline_audit_trail": []
        }
        
        return await app_graph.ainvoke(initial_runtime_state)
        
    except Exception as e:
       
        print("\n" + "="*50 + " GRAPH ERROR DETECTED " + "="*50)
        traceback.print_exc()
        print("="*122 + "\n")
        raise HTTPException(status_code=500, detail=f"War Room Pipeline Disruption: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api.server:app", host=settings.host, port=settings.port, reload=True)