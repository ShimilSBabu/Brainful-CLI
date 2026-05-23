def run(file_path:str, contents:str) -> dict:
    """This tool can write a new file when the file path and the contents are given."""

    with open(file_path, "a") as f:
        f.write(contents)
    return {"status":1}