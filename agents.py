import pandas as pd


# AGENT 1: SOIL ANALYSIS
def soil_agent(ph, nitrogen, phosphorus, potassium):
    if ph < 5.5:
        ph_status = "Acidic soil"
    elif ph > 7.5:
        ph_status = "Alkaline soil"
    else:
        ph_status = "Suitable pH range for many crops"

    npk_status = (
        f"Nitrogen: {nitrogen}, "
        f"Phosphorus: {phosphorus}, "
        f"Potassium: {potassium}"
    )

    return {
        "agent": "Soil Agent",
        "ph_status": ph_status,
        "npk_status": npk_status,
        "summary": f"{ph_status}. {npk_status}"
    }


# AGENT 2: WEATHER ANALYSIS
def weather_agent(temperature, rainfall):
    if temperature > 35:
        temperature_status = "High temperature: monitor heat stress"
    elif temperature < 10:
        temperature_status = "Low temperature: check cold-sensitive crops"
    else:
        temperature_status = "Temperature is moderate"

    if rainfall < 30:
        rainfall_status = "Low rainfall: irrigation may be needed"
    elif rainfall > 150:
        rainfall_status = "High rainfall: check drainage"
    else:
        rainfall_status = "Rainfall is moderate"

    return {
        "agent": "Weather Agent",
        "temperature_status": temperature_status,
        "rainfall_status": rainfall_status,
        "summary": f"{temperature_status}. {rainfall_status}."
    }


# AGENT 3: MARKET ANALYSIS
def market_agent(prices):
    prices = pd.Series(prices, dtype=float)

    if prices.empty:
        return {
            "agent": "Market Agent",
            "best_crop": "Not available",
            "summary": "No market price data available."
        }

    best_crop = prices.idxmax()

    return {
        "agent": "Market Agent",
        "best_crop": best_crop,
        "best_price": float(prices.max()),
        "summary": (
            f"{best_crop} has the highest price in the "
            f"provided sample data: ₹{prices.max():.2f} per quintal."
        )
    }


# AGENT 4: FARMING DECISION
def decision_agent(soil, weather, market):
    recommendations = []

    if "Acidic" in soil["ph_status"]:
        recommendations.append(
            "Test soil before deciding whether lime is needed."
        )

    if "Alkaline" in soil["ph_status"]:
        recommendations.append(
            "Check soil nutrient availability with a soil test."
        )

    if "High temperature" in weather["temperature_status"]:
        recommendations.append(
            "Consider suitable irrigation and heat-management practices."
        )

    if "Low rainfall" in weather["rainfall_status"]:
        recommendations.append(
            "Check soil moisture before scheduling irrigation."
        )

    if "High rainfall" in weather["rainfall_status"]:
        recommendations.append(
            "Check field drainage and waterlogging risk."
        )

    recommendations.append(
        f"Investigate {market['best_crop']} as a market option, "
        "after checking local growing suitability and costs."
    )

    return {
        "agent": "Decision Agent",
        "recommendations": recommendations
    }