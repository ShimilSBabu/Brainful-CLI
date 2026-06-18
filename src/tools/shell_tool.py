import subprocess
from langsmith import traceable

@traceable(run_type="tool")
def run(command:str, arguments:str|None = None, cwd:str|None = None)->dict:
    """This tool can perform shell command execution if command, arguments(if any) and cwd(if applicable) are given."""
    status=True
    error=""
    full_command = []
    try:
        if not "cmd /c" in command:
            full_command += ["cmd", "/c"]
        if arguments:
            full_command += [command] + [arguments]
        else:
            full_command += [command]
        result = subprocess.run(full_command,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    cwd=cwd,
                    shell=False
        )
        content=result.stdout
        metadata={
            "std_status":result.returncode==0,
            "std_err":result.stderr,
            "code":result.returncode
            }
    except Exception as e:
        status=False
        content=""
        metadata={}
        error=str(e)
    return {
        "status":status,
        "content":content,
        "error":error,
        "metadata":metadata
        }
    # return{
    #     "status":result.returncode==0,
    #     "stdout":result.stdout,
    #     "stderr":result.stderr,
    #     "code":result.returncode
    # }