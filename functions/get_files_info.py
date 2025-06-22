import os

def get_files_info(working_directory, directory=None):
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    
    directory_abs = os.path.abspath(directory)
    working_directory_abs = os.path.abspath(working_directory)

    if not directory_abs.startswith(working_directory_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    list_of_items = os.listdir(path=directory)
    output_string = ""

    for item in list_of_items:
        name = item
        size = str(os.path.getsize(os.path.join(directory, item)))
        type = not os.path.isfile(os.path.join(directory, item))
        output_string += f"- {name}: file_size={size} bytes, is_dir={type}\n"

    return output_string
            