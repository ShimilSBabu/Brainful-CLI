def run(file_path:str)->dict:
    """This tool can read and return the contents of a file when the file path is given."""

    with open(file_path, "r") as f:
        file_contents=f.read()
    return {"status":1, "content":file_contents}