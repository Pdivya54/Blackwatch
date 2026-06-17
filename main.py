import streamlit as st
from graph.pipeline import app_graph

st.title("Market Intelligence Dashboard")

# 1. Create input fields so the user can actually choose the company
brand_name = st.text_input("Brand Name:", "ADIDAS")
ticker_symbol = st.text_input("Ticker Symbol:", "ADDYY")

if st.button("Run Pipeline"):
    st.write(f"🤖 Initializing pipeline for {brand_name}...")

    # 2. Inject the USER input into the state, not the hardcoded strings
    dynamic_state = {
        "brand_name": brand_name.upper().strip(),
        "ticker_symbol": ticker_symbol.upper().strip(),
        "ad_campaign_data": {},
        "equity_risk_metrics": {},
        "threat_matrix_assessment": {},
        "proactive_mitigation_plan": {},
        "executive_brief_markdown": "",
        "next_agent": "",
        "pipeline_audit_trail": []
    }
    
    # 3. Run the pipeline with the dynamic state
    result = app_graph.invoke(dynamic_state)
    
    if result:
        st.write("🏁 Execution Complete!")
        st.json(result.get("pipeline_audit_trail"))
        st.markdown(result.get("executive_brief_markdown"))