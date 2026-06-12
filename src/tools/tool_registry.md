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
            "status":status,
            "content":content,
            "error":str(e),
            "metadata":{
                "std_status":result.returncode==0,
                "std_err":result.stderr,
                "code":result.returncode
                }
            }
    }

## read_document_tool
    {
        "name": "read_document_tool",
        "description":"This tool can read and return the contents of a file when the file path is given.",
        "all_parameters":{"file_path":str},
        "minimum_required_parameters":{"file_path":str},
        "output_structure":{
            "status":status,
            "content":file_contents,
            "error":str(e),
            "metadata":{}
        }
    }

## write_document_tool
    {
        "name": "write_document_tool",
        "description":"This tool can write a new file when the file path and the contents are given.",
        "all_parameters":{"file_path":str, "contents":str},
        "minimum_required_parameters":{"file_path":str, "contents":str},
        "output_structure":{
            "status":status,
            "content":"",
            "error":str(e),
            "metadata":{}
            }
    }

## modify_document_tool
    {
        "name": "modify_document_tool",
        "description":"This tool can append new content to the already present contents of a file when the file path and the additional contents are given.",
        "all_parameters":{"file_path":str, "additional_contents":str},
        "minimum_required_parameters":{"file_path":str, "additional_contents":str},
        "output_structure":{
            "status":status,
            "content":"",
            "error":str(e),
            "metadata":{}
        }
    }

## return_final_output_tool
    {
        "name": "return_final_output_tool",
        "description":"This tool returns the final output to the user. This tool must be madatorily called if the user needs to get the output for their query.",
        "all_parameters":{"content":str},
        "minimum_required_parameters":{"content":str},
        "output_structure":{
                "status":status,
                "content":final_output,
                "error":"",
                "metadata":{}
            }
    }