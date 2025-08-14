from typing import Dict, Any

# Mock FX rates vs USD for demo purposes
MOCK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "JPY": 155.0,
    "INR": 83.0,
    "GBP": 0.78
}

CONVERT_CURRENCY_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "convert_currency",
        "description": "Convert currency using mock exchange rates.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {"type": "number"},
                "from_currency": {"type": "string", "description": "e.g., 'USD'"},
                "to_currency": {"type": "string", "description": "e.g., 'JPY'"}
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    }
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """Mock currency conversion without external APIs."""

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in MOCK_RATES or to_currency not in MOCK_RATES:
        return {"error": f"Unsupported currency pair {from_currency}->{to_currency}"}

    amount_usd = amount / MOCK_RATES[from_currency]
    converted = amount_usd * MOCK_RATES[to_currency]

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": round(converted, 2),
        "note": "Mock rate for demo only"
    }
