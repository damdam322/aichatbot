import os
import subprocess

def run_python_file(working_directory, file_path):
    dic = os.path.abspath(os.path.join(working_directory, file_path))
    wd = os.path.abspath(working_directory)

    if os.path.commonpath([wd, dic]) != wd:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(dic):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python3", dic],
            capture_output=True,
            text=True,
            timeout=30
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    stdout = f"STDOUT: {result.stdout}" 
    stderr = f"STDERR: {result.stderr}"

    if result.returncode != 0:
        return f"Process exited with code {result.returncode}"
    if result.stdout == "" and result.stderr == "":
        return "No output produced."
    else:
        return f"{stdout}\n{stderr}"
    
    

