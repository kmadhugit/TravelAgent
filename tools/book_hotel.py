from datetime import datetime, timedelta
from typing import Optional, Dict, Any

BOOK_HOTEL_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "book_hotel",
        "description": "Book a hotel for the user in a destination city for a number of nights.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "City name, e.g., 'Tokyo'."},
                "nights": {"type": "integer", "description": "How many nights to stay."},
                "check_in_date": {"type": "string", "description": "Optional check-in date, e.g., '2025-08-20' or 'next Monday'."}
            },
            "required": ["destination", "nights"]
        }
    }
}

def book_hotel(destination: str, nights: int, check_in_date: Optional[str] = None) -> Dict[str, Any]:
    """Mock hotel booking tool. Pretends to contact providers and returns a reservation."""

    # Simple default check-in date: 7 days from now (UTC)
    if not check_in_date:
        check_in = datetime.utcnow().date() + timedelta(days=7)
        check_in_str = check_in.isoformat()
    else:
        # For the mock, just return the provided string
        check_in_str = check_in_date

    # Compute a mock check-out
    check_out_str = None
    try:
        if len(check_in_str) == 10:
            dt = datetime.strptime(check_in_str, "%Y-%m-%d").date()
            check_out_str = (dt + timedelta(days=nights)).isoformat()
    except Exception:
        pass

    return {
        "status": "confirmed",
        "hotel": "Grand Mock Hotel",
        "destination": destination,
        "nights": nights,
        "check_in": check_in_str,
        "check_out": check_out_str or f"{check_in_str} + {nights} nights",
        "confirmation_number": "MOCK-HOTEL-12345"
    }
