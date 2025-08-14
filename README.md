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



### OpenAI tool-calling: message flow, schemas, and roles

This repo uses OpenAI Chat Completions with function/tool calling to decide which tools to run, execute them locally, and then synthesize a final answer.

#### Message roles
- **system**: Sets high-level behavior and constraints. The model should follow this throughout the conversation.
- **user**: End-user input (prompts/questions/commands).
- **assistant**: Model responses. In the first turn, the assistant may return `tool_calls` instead of a final natural‑language reply.
- **tool**: Messages that contain the results of running a tool. Must include a `tool_call_id` that matches the assistant’s tool call.

#### End-to-end call sequence
1) Build the initial messages and call the model with tool schemas and `tool_choice="auto"`:
```python
first = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "...policy..."},
        {"role": "user", "content": user_text},
    ],
    tools=TOOLS,            # JSON Schemas for available tools
    tool_choice="auto",    # The model decides which tools to call
    temperature=0,
)
```

2) If the assistant returns `tool_calls`, execute them locally, then append:
- The original assistant message (which contains `tool_calls`)
- One `role: tool` message per tool call, with matching `tool_call_id` and the tool’s JSON result as string content

3) Make a second call without `tools` to ask the model to synthesize the final natural‑language answer.

#### Tool schema (input to OpenAI)
Each tool is declared using the Chat Completions tools format with JSON Schema for parameters:
```json
{
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
```
In this project, `TOOLS` is a list of such tool specs aggregated in `tools/tool_factory.py`.

#### Messages schema (input to OpenAI)
The `messages` array uses the Chat Completions format:
```json
[
  {"role": "system", "content": "You are a precise travel assistant..."},
  {"role": "user", "content": "Book me a hotel in Tokyo for 3 nights and what's the weather?"}
]
```

When sending tool results back, each tool execution is appended as:
```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"status\":\"confirmed\",\"destination\":\"Tokyo\"}"
}
```
Note: `content` is a string. This project `json.dumps(...)` the tool result before attaching it.

#### Assistant tool calls (output from first OpenAI call)
The first assistant message may include `tool_calls` instead of final text:
```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\":\"Tokyo\"}"
      }
    },
    {
      "id": "call_def456",
      "type": "function",
      "function": {
        "name": "book_hotel",
        "arguments": "{\"destination\":\"Tokyo\",\"nights\":3}"
      }
    }
  ]
}
```
Your app is responsible for parsing `function.arguments` (JSON), running the tool locally, and attaching the results with matching `tool_call_id`.

#### Final assistant response (output from second OpenAI call)
After appending all tool results, call the model again (no `tools`). The response will be standard assistant text:
```json
{
  "role": "assistant",
  "content": "You are booked at Grand Mock Hotel in Tokyo... The forecast is Sunny with light breeze."
}
```

#### Minimal end-to-end example
```python
messages = [
  {"role": "system", "content": "You are a precise travel assistant."},
  {"role": "user", "content": "Book a hotel in Tokyo for 3 nights and what's the weather?"},
]

first = client.chat.completions.create(
  model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto", temperature=0
)

tool_calls = first.choices[0].message.tool_calls or []
if tool_calls:
    # Run tools
    messages.append(first.choices[0].message)
    for tc in tool_calls:
        name = tc.function.name
        args = json.loads(tc.function.arguments or "{}")
        result = execute_tool_call(tc)["result"]
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": json.dumps(result)
        })

    second = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    print(second.choices[0].message.content)
else:
    print(first.choices[0].message.content)
```

#### Notes on behavior
- The model decides which tools to call and the arguments to pass based on your prompt and tool schemas.
- Always pass tool results back as `role: tool` with the exact `tool_call_id` from the assistant’s request.
- Keep tool results concise and JSON-serializable so the model can reliably read them.

