import os
import json
import asyncio
from dotenv import load_dotenv
from src.cli import CLI
from google import genai
from google.genai import types
from src.toolkit import tools  # Your tools list (some can be async)

# Load environment
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

# Config
MAX_HISTORY = 10
client = genai.Client(api_key=API_KEY)
history = []

# Utility
def Message(role, content):
    return {"role": role, "content": content}

# System Prompt
PROMPT = Message(role="system", content=(
    'Respond to the user query  **strictly** in JSON Convertible format string '
    '{"response":RESPONE ,"args":ARGS ,"tool_name":TOOL_NAME} where RESPONE is the response to the user query, '
    'and TOOL_NAME is the name of the tool to use, ARGS are the arguments for the next action which should be in an array, '
    'If no tool is needed, set TOOL_NAME to None and ARGS to None.\n'
    'Example: {"tool_name":"file_writer","args":["file","hello"],"response":"Calling File Writer"}\n'
    # 'If the previous message was a tool response, then you should not use any tool and just return the response.\n'
))
tool_prompt = "\nYou can use the following tools:\n"
for tool in tools:
    tool_prompt += f"{tool.__name__}: {tool.__doc__} "
PROMPT["content"] += tool_prompt


# -------------------------------
# Async LLM Call
# -------------------------------
async def llm():
    # [print(f"{msg['role']}: {msg['content']}") for msg in history[-MAX_HISTORY:]]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"{msg['role']}: {msg['content']}" for msg in history[-max(MAX_HISTORY,len(history)-1):]],
        config=types.GenerateContentConfig(
            system_instruction=[PROMPT['content']],
        )
    )
    text = response.candidates[0].content.parts[0].text
    text = text.strip()

    try:
        parsed = json.loads(text.strip().strip('`').replace("json\n", "", 1).strip())
    except json.JSONDecodeError:
        history.append(Message("system", "Could not parse JSON. Your last response: " + text))
        return

    ai = Message(role="model", content=parsed["response"])

    # If a tool needs to be used
    if parsed["tool_name"] is not None and parsed["args"] is not None:
        ai["response"] = f"Executing tool: {parsed['tool_name']} with args: {parsed['args']}"
        history.append(ai)

        tool_response = Message(role="tool", content="")

        # Find tool function
        tool_func = next((t for t in tools if t.__name__ == parsed["tool_name"]), None)
        if tool_func:
            try:
                # Await if it's an async function
                if asyncio.iscoroutinefunction(tool_func):
                    result = await tool_func(*parsed["args"])
                else:
                    result = tool_func(*parsed["args"])
            except Exception as e:
                result = f"Error during tool execution: {e}"
        else:
            result = f"Tool {parsed['tool_name']} not found."

        tool_response["content"] = result
        history.append(tool_response)
        await llm()
    else:
        history.append(ai)


# -------------------------------
# Loop
# -------------------------------
async def loop():
    while True:
        inp = input(CLI.bold("User: "))
        if inp.lower() in ("exit", "quit"):
            break
        history.append(Message("user", inp))
        await llm()
        print(CLI.bold("Assistant:"), CLI.info(history[-1]["content"]))

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    asyncio.run(loop())
