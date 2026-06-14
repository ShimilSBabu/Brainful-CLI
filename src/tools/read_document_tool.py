from langsmith import traceable

@traceable(run_type="tool")
def run(file_path:str)->dict:
    """This tool can read and return the contents of a file when the file path is given."""
    status=True
    error=""
    try:
        with open(file_path, "r") as f:
            file_contents=f.read()
    except Exception as e:
        status=False
        error=str(e)
    return {
            "status":status,
            "content":file_contents,
            "error":error,
            "metadata":{}
        }