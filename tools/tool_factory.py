import json
from typing import Dict, Any, List

from tools.book_hotel import book_hotel, BOOK_HOTEL_TOOL_SCHEMA
from tools.get_weather import get_weather, GET_WEATHER_TOOL_SCHEMA
from tools.convert_currency import convert_currency, CONVERT_CURRENCY_TOOL_SCHEMA

# Compose tool schemas from individual modules
TOOLS: List[Dict[str, Any]] = [
    BOOK_HOTEL_TOOL_SCHEMA,
    GET_WEATHER_TOOL_SCHEMA,
    CONVERT_CURRENCY_TOOL_SCHEMA,
]

def execute_tool_call(tool_call) -> Dict[str, Any]:
    """Run one tool call and return its result tied to tool_call_id."""
    name = tool_call.function.name
    try:
        args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError:
        args = {}
    if name == "book_hotel":
        result = book_hotel(**args)
    elif name == "get_weather":
        result = get_weather(**args)
    elif name == "convert_currency":
        result = convert_currency(**args)
    else:
        result = {"error": f"Unknown tool: {name}"}
    return {"tool_call_id": tool_call.id, "name": name, "result": result}


