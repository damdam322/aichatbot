import os
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    dic = os.path.join(working_directory, file_path)
    if not os.path.abspath(dic).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(dic):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(dic, "r") as f:
        file_content = f.read(MAX_CHARS)
    if len(file_content) == 10000:
        return f"{file_content}\n[...File {file_path} truncated at 10000 characters]"
    else:
        return file_content