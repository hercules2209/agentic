from pathlib import Path
from functions.typeUnions import StrOrPath
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory:str, file_path:StrOrPath):
    try:
        base = Path(working_directory).resolve()
        d = Path(file_path)

        if d.is_absolute():
            file_path = d.resolve()
        else:
            file_path = (base / d).resolve()

        if not file_path.is_relative_to(base):
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not file_path.exists or not file_path.is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file_path, 'r') as f:
            content = f.read(MAX_CHARS+1)

        return content if len(content)<=MAX_CHARS else content[:MAX_CHARS]+f'\n[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve, relative to the working directory. If not provided, retrieves the content of the file in the working directory itself.",
            ),
        },
    ),
)
