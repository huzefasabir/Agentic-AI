

from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_google_genai  import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()


import asyncio

# Resolve absolute path to mathserver.py so it works regardless of CWD
MATH_SERVER_PATH = str(Path(__file__).parent / "mathserver.py")
async def main():
    client=MultiServerMCPClient(
        {
            # Math server: uses stdio transport — spawns mathserver.py as a subprocess
            "math": {
                "command": "python",
                "args": [MATH_SERVER_PATH],
                "transport": "stdio",
            },
            # Weather server: uses streamable-http — run `python weather.py` first (serves on port 8000)
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    tools = await client.get_tools()
    print(f"Available tools: {[t.name for t in tools]}")

    llm_gem = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    agent = create_react_agent(llm_gem, tools)

    math_response=await agent.ainvoke(
        {
            "messages":[{"role":"user","content":"What is (3+5) * 12 "}]
        }
    )

    weather_resp= await agent.ainvoke(
        {
            "messages":[{
                "role":"user", "content":"What is the weather like in new york city"
            }]
        }
    )

    print("Math Response:", math_response["messages"][-1].content)
    print("Weather Response:", weather_resp["messages"][-1].content)

asyncio.run(main())