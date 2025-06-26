import os

def get_files_info(working_directory, directory=""):
    dic = os.path.abspath(os.path.join(working_directory, directory))
    wd = os.path.abspath(working_directory)

    if not os.path.isdir(dic):
        return f'Error: "{directory}" is not a directory'

    if os.path.commonpath([wd, dic]) != wd:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    list_of_items = os.listdir(path=dic)
    output_string = ""

    for item in list_of_items:
        name = item
        size = str(os.path.getsize(os.path.join(dic, item)))
        type = not os.path.isfile(os.path.join(dic, item))
        output_string += f"- {name}: file_size={size} bytes, is_dir={type}\n"

    return output_string
            