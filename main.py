import os
import sys
from const_virables import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from dotenv import load_dotenv
from google import genai
from google.genai import types

#check for input
verbose = False
if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("usage: python3 main.py \"your prompt\", optional: --verbose")
        sys.exit(1)
elif len(sys.argv) == 3:
    if sys.argv[2] == "--verbose":
        verbose = True
    else:
        print("invalid third flag did you mean --verbose?")
        sys.exit(1)

#load api key and initialize
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schemas = [
    types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    ),
    types.FunctionDeclaration(
        name="get_file_content",
        description="reads content of a file up to 10000 characters, files are constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to read content out of, relative to the working directory",
                ),
            },
        ),
    ),
    types.FunctionDeclaration(
        name="write_file",
        description="creates a file with content or overwrites if file exist, this function is constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to file to be overwritten with content or created with content, relative to the working directory",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="content for a file to be created with or be overwritten with",
                ),
            },
        ),
    ),
    types.FunctionDeclaration(
        name="run_python_file",
        description="runs python file python files endswith .py, python files are constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to file, relative to the working directory if user dont provide path just insert here filename it will work",
                ),
            },
        ),
    ),
]

available_functions = types.Tool(
    function_declarations=schemas
)

def call_function(call, verbose=False):
    if verbose:
        print(f"Calling function: {call.name}({call.args})")
    else:
        print(f" - Calling function: {call.name}")

    match call.name:
        case "get_files_info":
            result = f"{get_files_info(WORKING_DIRECTORY, **call.args)}"
        case "get_file_content":
            result = f"{get_file_content(WORKING_DIRECTORY, **call.args)}"
        case "write_file":
            result = f"{write_file(WORKING_DIRECTORY, **call.args)}"
        case "run_python_file":
            result = f"{run_python_file(WORKING_DIRECTORY, **call.args)}"
        case _:
            return types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                            name=call.name,
                            response={"error": f"Unknown function: {call.name}"},
                            )
                        ],
                    )
            
    return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                    )
                ],
            )

def response_parsed(verbose=False):
    output_string = response.text

    if verbose:
        output_string += f"\nUser prompt: {sys.argv[1]}"
        output_string += f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}"
        output_string += f"\nResponse tokens: {response.usage_metadata.candidates_token_count}"

    return output_string

messages = [
    types.Content(
    role="user",
    parts=[
        types.Part(
            text=sys.argv[1]
        )
    ]
    ),
]

response = client.models.generate_content(
            model= "gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT
            )
        )

def main():
    global messages
    global response
    
    for i in range(MAX_ITERATIONS):

        response = client.models.generate_content(
            model= "gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT
            )
        )

        map(lambda candid: messages.append(candid.content), response.candidates)

        if response.function_calls is None:
            print(response_parsed(verbose))
            break
        else:
            function_call_result = call_function(response.function_calls[0], verbose)
            if function_call_result.parts[0].function_response.response is None:
               raise Exception("fatal error")
            elif verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)

    return



if __name__ == '__main__':
  main()
  sys.exit(0)