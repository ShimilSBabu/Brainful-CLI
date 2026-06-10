def run(file_path:str, additional_contents:str) -> dict:
    """This tool can append new content to the already present contents of a file when the file path and the additional contents are given."""

    status=True
    try:
        with open(file_path, "a") as f:
            f.write(additional_contents)
    except Exception as e:
        status=False
    return {
            "status":status,
            "content":"",
            "error":str(e),
            "metadata":{}
        }