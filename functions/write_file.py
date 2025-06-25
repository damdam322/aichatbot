import os

def write_file(working_directory, file_path, content):
    dic = os.path.join(working_directory, file_path)
    if not os.path.abspath(dic).startswith(os.path.abspath(working_directory)):
        return f"Cannot write to {file_path} as it is outside the permitted working directory"
    if not os.path.exists(dic):
        if os.makedirs(dic)