import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# How to launch the server (Phase 0)
server_params = StdioServerParameters(
    command=sys.executable,   # the python you run this with (your venv)
    args=["server.py"],
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()                    # handshake

            tools = await session.list_tools()            # discovery
            print("TOOLS:")
            for t in tools.tools:
                print(f" - {t.name}: {t.description}")

            result = await session.call_tool("add", {"a": 5, "b": 3})   # execution
            print("add(5, 3) =", result.content[0].text)

asyncio.run(main())