import os
import sys
from const_virables import SYSTEM_PROMPT, WORKING_DIRECTORY
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from dotenv import load_dotenv
from google import genai
from google.genai import types

#check for input
if len(sys.argv) < 2:
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
                    description="The file_path to read content out of, relative to the working directory",
        ),
            },
        ),
    )
]


available_functions = types.Tool(
    function_declarations=schemas
)

messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),]

response = client.models.generate_content(
    model= "gemini-2.0-flash-001", 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=SYSTEM_PROMPT
        )
    )

def print_response():
    if len(response.function_calls) != 0:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
            match call.name:
                case "get_files_info":
                    print(get_files_info(WORKING_DIRECTORY, **call.args))
                    break
                case "get_file_content":
                    print(get_file_content(WORKING_DIRECTORY, **call.args))


    print(response.text)

    if len(sys.argv) == 3:
         if sys.argv[2] == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    return

def main():
    print_response()

if __name__ == '__main__':
  main()
  sys.exit(0)