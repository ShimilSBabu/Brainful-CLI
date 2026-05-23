import subprocess

def run(command:str, arguments:str|None = None, cwd:str|None = None)->dict:
    """This tool can perform shell command execution if command, arguments(if any) and cwd(if applicable) are given."""
    full_command = [command] + arguments
    result = subprocess.run(full_command,
                capture_output=True,
                text=True,
                timeout=20,
                cwd=cwd,
                shell=False
    )

    return{
        "status":result.returncode==0,
        "stdout":result.stdout,
        "stderr":result.stderr,
        "code":result.returncode
    }