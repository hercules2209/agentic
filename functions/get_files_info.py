from pathlib import Path
from typing import Optional
from functions.typeUnions import StrOrPath
from google.genai import types

def get_files_info(working_directory:str, directory:Optional[StrOrPath] = None) -> str:
    try:
        base = Path(working_directory).resolve()
        if directory is None:
            target = base
        else:
            d = Path(directory)
            target = d.resolve() if d.is_absolute() else (base / d).resolve()


        if not target.exists() or not target.is_dir():
            return f'Error: "{directory}" is not a directory'
    
        if not target.is_relative_to(base):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        files_info:list[str]=[]
        for p in target.iterdir():
            size = p.stat().st_size
            is_dir: bool = p.is_dir()
            files_info.append( f'{p.name}: file_size={size} bytes, is_dir={is_dir}\n')
        return f'Info: {target} is empty' if not files_info else "\n".join(files_info)
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
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
)
