from langsmith import traceable

@traceable(run_type="tool")
def run(file_path:str, contents:str) -> dict:
    """This tool can append new content to the already present contents of a file when the file path and the additional contents are given."""

    status=True
    error=""
    try:
        with open(file_path, "a") as f:
            f.write(contents)
    except Exception as e:
        status=False
        error=str(e)
    return {
            "status":status,
            "content":"",
            "error":error,
            "metadata":{}
        }