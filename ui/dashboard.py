# This script builds the interactive user interface dashboard using Streamlit to serve as an executive control deck.
# It captures user parameters, handles async HTTP communication with the FastAPI backend, and renders live logs, markdown reports, and simulation metrics.


import streamlit as st
import requests

st.set_page_config(page_title="BLACKWATCH // Strategic Horizon", layout="wide", initial_sidebar_state="expanded")

st.title(" PROJECT BLACKWATCH: PREDICTIVE COMMAND CENTER")
st.subheader("Continuous Autonomous Threat Forecasting & Proactive Mitigation Loop")
st.markdown("---")

with st.sidebar:
    st.header(" CONTROLS")
    brand_input = st.text_input("Target Competitor Identity:", value="Nike")
    ticker_input = st.text_input("Equity Asset Ticker Symbol:", value="NKE")
    st.markdown("---")
    backlash_slider = st.slider("Public Backlash Level Multiplier", 1.0, 10.0, 6.0, step=0.5)
    execute_signal = st.button("RUN PREDICTIVE SYSTEM EVALUATION")

col_metrics, col_display = st.columns([1, 2])

with col_metrics:
    st.markdown("###  Live Radar Status")
    st.metric(label="System Guard Status", value="PREDICTIVE ACTIVE", delta="SECURE")
    if not execute_signal:
        st.info("Awaiting execution target confirmation.")

if execute_signal:
    with st.spinner(" Forecasting Time Horizons & Drafting Proactive Copy Plans..."):
        try:
            
            res = requests.post(
                "http://127.0.0.1:8000/api/v1/intercept",
                json={
                    "brand_name": brand_input, 
                    "ticker_symbol": ticker_input,
                    "simulation_modifiers": {"backlash_index": backlash_slider / 10.0}
                },
                timeout=120
            )
            
            if res.status_code == 200:
                data = res.json()
                
                with col_metrics:
                    threat_score = data.get("threat_matrix_assessment", {}).get("derived_threat_level", "UNKNOWN")
                    st.warning(f"###  FORECASTED POSTURE: {threat_score}")
                    
                    st.info("###  Agent Routing History Trail")
                    for trace_log in data.get("pipeline_audit_trail", []):
                        st.caption(f"➔ {trace_log}")
                        
                with col_display:
                    st.success("### STRATEGIC PREDICTIVE ASSESSMENT BRIEF")
                    st.markdown(data.get("executive_brief_markdown"))
                    
                    forecast_list = data.get("threat_matrix_assessment", {}).get("predictive_forecast_data", [])
                    if forecast_list:
                        st.markdown("---")
                        st.markdown("### FORWARD-LOOKING RISK HORIZON MATRIX")
                        
                        table_html = """
| Interval Horizon | Projected Stock Floor | Estimated Value Loss | Operational Defense Posture |
| :--- | :--- | :--- | :--- |
"""
                        
                        for item in forecast_list:
                            table_html += f"| **{item['day']}** | ${item['projected_asset_floor']} | -{item['variance_impact_pct']}% | `{item['recommended_posture']}` |\n"
                        
                        st.markdown(table_html)
            else:
                st.error("Intercept Pipeline split. Server returned an unparseable data packet.")
        except Exception:
            st.error("Connection Severed. Ensure the Core Blackwatch Server node is listening on local port 8000.")