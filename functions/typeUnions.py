from typing import Union, List, Tuple
from google.genai import types
from pathlib import Path

StrOrPath = Union[str, Path]

FunctionResponse = Tuple[
  str,
  List[types.FunctionCall],
  List[types.Candidate],
  int | None,
  int | None
]
