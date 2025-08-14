import os
import json
from typing import Dict, Any, List
from openai import OpenAI

# Tool implementations (mock/no external APIs)
from tools.tool_factory import TOOLS, execute_tool_call
from user_inputs import USER_INPUTS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

 

def handle_user_query(user_text: str) -> str:
    # 1) Ask the model which tools to call (it can call multiple in one response)
    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a precise travel assistant. "
                "If multiple intents are present, call multiple tools. "
                "You can call the tools in any order you want."
            ),
        },
        {
            "role": "user",
            "content": user_text            
        },
    ]
    print("--------------MSG TO OPENAI---------------")
    print(messages)

    first = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0
    )

    print("--------------MSG FROM OPENAI---------------")
    print(first)
    
    tool_calls = first.choices[0].message.tool_calls or []

    if tool_calls:
        # 2) Execute tool calls sequentially (simple, synchronous)
        results = [execute_tool_call(tc) for tc in tool_calls]

        # 3) Include the assistant message that contained the tool calls
        messages.append(first.choices[0].message)

        # 4) Append tool results and ask the model to produce a final response
        for r in results:
            messages.append({
                "role": "tool",
                "tool_call_id": r["tool_call_id"],
                "content": json.dumps(r["result"])
            })

        print("--------------NEW MSG TO OPENAI---------------")
        print(messages)

        

        second = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0
        )

        print("--------------NEW MSG FROM OPENAI---------------")
        print(second)


        return second.choices[0].message.content or ""
    else:
        # No tools needed
        return first.choices[0].message.content or ""

def main():
    print("✨ Travel Assistant. Running predefined user inputs...")
    for idx, user_text in enumerate(USER_INPUTS, start=1):
        print(f"\n=== Input {idx} ===\n> {user_text}")
        reply = handle_user_query(user_text)
        print(f"\nAssistant:\n{reply}")

if __name__ == "__main__":
    main()
 

