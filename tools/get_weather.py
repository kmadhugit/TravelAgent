from typing import Optional, Dict, Any

GET_WEATHER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get a simple weather forecast for a city on a given date (mock data).",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "date": {"type": "string", "description": "Optional date, e.g., '2025-08-22' or 'next weekend'."}
            },
            "required": ["city"]
        }
    }
}

def get_weather(city: str, date: Optional[str] = None) -> Dict[str, Any]:
    """Mock weather tool. Returns a simple forecast without real API calls."""

    conditions = "Sunny with light breeze"
    if city.lower() in {"london", "seattle"}:
        conditions = "Cloudy with light rain"
    elif city.lower() in {"dubai"}:
        conditions = "Hot and dry"
    elif city.lower() in {"tokyo"}:
        conditions = "Partly cloudy, mild"

    return {
        "city": city,
        "date": date or "upcoming",
        "forecast": conditions,
        "high_c": 26,
        "low_c": 18
    }
