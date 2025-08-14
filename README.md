## Travel Assistant (Tool-Calling Demo)

This is a minimal CLI that demonstrates OpenAI tool-calling with synchronous tool execution. The assistant decides which tools to call from the user’s intent, runs them, and then synthesizes a final answer.

### How it works
1. Build a conversation with a system message and the user message.
2. First model call includes `tools` and `tool_choice="auto"`.
3. If the model returns `tool_calls`, each is executed synchronously in Python.
4. The original assistant message (that contains `tool_calls`) is appended back to the conversation.
5. Each tool result is appended as a `role: tool` message with the matching `tool_call_id`.
6. A second model call produces the final natural-language reply.

### Project structure
- `TravelAgent.py`: Orchestrates model calls, executes tool calls, and prints responses.
- `tools/tool_factory.py`: Exports `TOOLS` (schemas) and `execute_tool_call` (dispatcher).
- `tools/book_hotel.py`: Mock hotel booking tool and `BOOK_HOTEL_TOOL_SCHEMA`.
- `tools/get_weather.py`: Mock weather tool and `GET_WEATHER_TOOL_SCHEMA`.
- `tools/convert_currency.py`: Mock currency conversion tool and `CONVERT_CURRENCY_TOOL_SCHEMA`.
- `user_inputs.py`: Predefined inputs that trigger 0, 1, or multiple tool calls.
- `requirements.txt`: Python dependencies.

### Tool-calling details
- Tool schemas live beside their implementations (one module per tool) and are aggregated in `tools/tool_factory.py`.
- Execution is synchronous and simple: each tool call is mapped by name to its function.
- Tool results are JSON-serialized when appended to the conversation with `role: tool`.

### Run
Prereqs:
- Python 3.10+
- `OPENAI_API_KEY` exported in your shell (e.g. in `.profile`, `.zshrc`, etc.)

Install and run:
```bash
pip install -r requirements.txt
python TravelAgent.py
```

The app iterates through `USER_INPUTS` in `user_inputs.py` to demonstrate different tool-calling scenarios.

### Add a new tool
1. Create a new module under `tools/`, e.g. `tools/plan_route.py`.
2. Implement a function (e.g. `plan_route(...)`) and export a schema constant named `PLAN_ROUTE_TOOL_SCHEMA`.
3. In `tools/tool_factory.py`:
   - Import the function and schema
   - Append the schema to `TOOLS`
   - Add a branch in `execute_tool_call` for the new tool name
4. (Optional) Add a new line in `user_inputs.py` to exercise the tool.

### Notes
- No `dotenv` is used; `OPENAI_API_KEY` is read directly from the environment.
- This sample uses mock tools only (no external API calls).


