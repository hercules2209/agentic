import subprocess
from pathlib import Path
from functions.typeUnions import StrOrPath
from google.genai import types

def run_python_file(working_directory:str, file_path: StrOrPath)->str:
    try:
        base = Path(working_directory).resolve()

        p = Path(file_path)
        if not p.is_absolute():
            target = (base / p).resolve()
        else:
            target = p.resolve()
        if not target.is_relative_to(base):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not target.exists():
            return f'Error: File "{file_path}" not found.'
        if target.suffix.lower()!=".py":
            return f'Error: "{file_path}" is not a Python file.'
        try:
           proc = subprocess.run(
                ["python3", str(target)],
                cwd=str(base),
                capture_output=True,
                text=True,
                timeout=30
            )
        except Exception as e:
            return f"Error: executing Python file: {e}"
        parts = []
        # STDOUT
        if proc.stdout:
            parts.append("STDOUT:\n" + proc.stdout.rstrip())
        # STDERR
        if proc.stderr:
            parts.append("STDERR:\n" + proc.stderr.rstrip())
        # Exit code
        if proc.returncode != 0:
            parts.append(f"Process exited with code {proc.returncode}")

        if not parts:
            return "No output produced."

        return "\n\n".join(parts)

    except Exception as e:
        return f'Error: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory. If not provided, executes the file in the working directory itself.",
            ),
        },
    ),
)
