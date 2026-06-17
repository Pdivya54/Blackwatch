# This file contains the quantitative analytical tools and data retrieval engines for the system.
# It fetches live market metrics using yfinance, extracts risk indexes, and models a square-root time decay curve for forward-looking asset projections.


import yfinance as yf
import math
from typing import Dict, Any, List

def get_brand_market_data(brand_name: str) -> Dict[str, Any]:
   
    return {
        "ad_attack_intensity": "MEDIUM", 
        "campaign_theme": f"Market analysis for {brand_name.upper()}", 
        "backlash_index": 0.05
    }
def calculate_equity_volatility(ticker: str) -> Dict[str, Any]:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")
        if hist.empty:
            return {"error": "Target entity tracking index not found."}
        
        close_prices = hist["Close"]
        returns = close_prices.pct_change().dropna()
        annualized_vol = float(returns.std() * (252 ** 0.5))
        
        return {
            "baseline_volatility_pct": round(annualized_vol * 100, 2),
            "asset_trend_direction": "BULLISH" if close_prices.iloc[-1] > close_prices.iloc[0] else "BEARISH",
            "last_closing_value": round(float(close_prices.iloc[-1]), 2)
        }
    except Exception as e:
        return {"error": str(e)}

def project_future_risk_curve(current_price: float, volatility: float, backlash_multiplier: float) -> List[Dict[str, Any]]:
    daily_decay = (volatility / 100.0) * (backlash_multiplier * 0.15)
    projections = []
    
    for day in [1, 5, 10, 30, 60]:
        impact_factor = 1.0 - (daily_decay * math.sqrt(day))
        projected_value = max(current_price * impact_factor, 1.00)
        
        if impact_factor < 0.85:
            posture = "CRITICAL DEGRADATION"
        elif impact_factor < 0.95:
            posture = "MATERIAL EXPOSURE"
        else:
            posture = "STABLE CORRIDOR"
            
        projections.append({
            "day": f"Day {day}",
            "projected_asset_floor": round(projected_value, 2),
            "variance_impact_pct": round((1.0 - impact_factor) * 100, 1),
            "recommended_posture": posture
        })
    return projections