def read_tool_registry():
    """This function provides necessary information regarding all the available tools."""
    with open("tools/tool_registry.md", "r") as f:
        tool_info = f.read()
    return tool_info