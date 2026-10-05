from mcp.server.fastmcp import FastMCP
from mcp_server.graph_tools import register_graph_tools
from mcp_server.memory_tools import register_memory_tools
from mcp_server.brain_tools import register_brain_tools
from mcp_server.action_tools import register_action_tools

mcp = FastMCP("SentinelGraph MCP")

register_graph_tools(mcp)
register_memory_tools(mcp)
register_brain_tools(mcp)
register_action_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse") # or standard
