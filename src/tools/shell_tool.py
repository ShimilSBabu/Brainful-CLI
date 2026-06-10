import subprocess

def run(command:str, arguments:str|None = None, cwd:str|None = None)->dict:
    """This tool can perform shell command execution if command, arguments(if any) and cwd(if applicable) are given."""
    status=True
    try:
        if arguments:
            full_command = [command] + [arguments]
        else:
            full_command = [command]
        result = subprocess.run(full_command,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    cwd=cwd,
                    shell=False
        )
    except Exception as e:
        status=False
    return {
        "status":status,
        "content":result.stdout,
        "error":str(e),
        "metadata":{
            "std_status":result.returncode==0,
            "std_err":result.stderr,
            "code":result.returncode
            }
        }
    # return{
    #     "status":result.returncode==0,
    #     "stdout":result.stdout,
    #     "stderr":result.stderr,
    #     "code":result.returncode
    # }