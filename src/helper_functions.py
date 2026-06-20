import os, json
from langchain_core.tools import StructuredTool
from importlib import import_module
from langsmith import traceable


def read_tool_registry():
    """This function provides necessary information regarding all the available tools."""
    with open(os.path.join("src", "tools", "tool_registry.md"), "r") as f:
        tool_info = f.read()
    return tool_info

@traceable
def fetch_task_result(task_id:str, tasks):
    """This function fetches the result of a previous task if the id of the previous task is mentioned."""
    for task in tasks:
        if task.id == task_id:
            return task.result if task.result else task.error
    return False


def tool_registry_generator(tool_directory_path):
    pass


def get_tools_info():
    """This function creates a list of dicctionary containing a necessary information regarding all the available tools."""

@traceable
def fetch_structuredtools():
    tools = []
    print(os.getcwd())
    file_path = os.path.join(os.getcwd(),"src", "tools")
    print(f"file_path: {file_path}")
    for file in os.listdir(path=file_path):
        if file.endswith(".py"):
            module_name=file.split(".py")[0]
            module=import_module(f"src.tools.{module_name}", package=__package__)
            tool = StructuredTool.from_function(
                func=module.run,
                # name=module.__name__,
                name=module_name,
                description=module.run.__doc__
            )
            tools.append(tool)
    return tools

# def read_tool_reg_as_json():

#     md = MarkdownIt()

#     with open(os.path.join("src", "tools", "tool_registry.md"), "r", encoding="utf-8") as f:
#         content = f.read()

#     tokens = md.parse(content)
#     data = [token.content for token in tokens if token.content.startswith("{")]
#     return data