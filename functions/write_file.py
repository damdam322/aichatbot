import os

def write_file(working_directory, file_path, content):
    dic = os.path.join(working_directory, file_path)
    if not os.path.abspath(dic).startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"
    
    #validate if path is file path
    is_end_file = False
    try:
        for i in reversed(dic):
            if i == "/" and is_end_file == False:
                return f"Cannot write to {file_path} file path is not file path example invalid: path/path valid: path/file.txt"
            if i == "/" and is_end_file:
                break
            if i == ".":
                is_end_file = True

        if os.path.exists(dic):
            with open(dic, "w") as f:
                f.write(content)
        else:
            os.makedirs(os.path.dirname(dic), exist_ok=True)
            f = open(dic, "w")
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    
