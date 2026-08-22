"""快速测试：MCP 协议连 set_alarm_clock.py，list_tools + call_tool。"""
import asyncio
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    env = dict(os.environ)
    env["JADE_ATTACK_TYPE"] = "DirectPoisoning"
    env["JADE_ATTACK_ID"] = "0"
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["set_alarm_clock.py"],
        cwd=HERE,
        env=env,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"工具数: {len(tools.tools)}")
            for t in tools.tools:
                print(f"  name={t.name}")
                print(f"  description={t.description}")
                print(f"  inputSchema={t.inputSchema}")
            res = await session.call_tool("set_alarm_clock", {"time": "18:00"})
            print(f"call result: {res}")


if __name__ == "__main__":
    asyncio.run(main())
