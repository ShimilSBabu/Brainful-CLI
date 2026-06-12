def run(file_path:str, contents:str) -> dict:
    """This tool can write a new file when the file path and the contents are given."""

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