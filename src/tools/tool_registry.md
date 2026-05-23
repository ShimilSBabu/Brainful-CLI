# Tool Registry
## shell_tool
    {
        "name": "shell_tool",
        "description":"This tool can perform shell command execution if command, arguments(if any) and cwd(if applicable) are given.",
        "all_parameters":{"command":str, 
            "arguments":str|None = None, 
            "cwd":str|None = None"
        },
        "minimum_required_parameters":{"command":str},
        "output_structure":{
            "status":result.returncode==0,
            "stdout":result.stdout,
            "stderr":result.stderr,
            "code":result.returncode
        }
    }

## read_document_tool
    {
        "name": "read_document_tool",
        "description":"This tool can read and return the contents of a file when the file path is given.",
        "all_parameters":{"file_path":str},
        "minimum_required_parameters":{"file_path":str},
        "output_structure":{"status":1, "content":file_contents}
    }

## write_document_tool
    {
        "name": "write_document_tool",
        "description":"This tool can write a new file when the file path and the contents are given.",
        "all_parameters":{"file_path":str, "contents":str},
        "minimum_required_parameters":{"file_path":str, "contents":str},
        "output_structure":{"status":1}
    }

## modify_document_tool
    {
        "name": "modify_document_tool",
        "description":"This tool can append new content to the already present contents of a file when the file path and the additional contents are given.",
        "all_parameters":{"file_path":str, "additional_contents":str},
        "minimum_required_parameters":{"file_path":str, "additional_contents":str},
        "output_structure":{"status":1}
    }
