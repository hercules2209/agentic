from pathlib import Path
from functions.typeUnions import StrOrPath
from google.genai import types

def write_file(working_directory:str, file_path:StrOrPath, content:str)->str:
    try:
        base = Path(working_directory).resolve()

        p = Path(file_path)
        if p.is_absolute():
            target = p.resolve()
        else:
            target = (base / p).resolve()

        if not target.is_relative_to(base):
            return f'Error: Cannot write to "{target}" as it is outside the permitted working directory'
        try:
            if not target.exists: 
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
        except Exception as e:
            return "Error: error creating file {e}"
        with open(target, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. If not provided, writes to a file in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            )
        }
    ),
)
