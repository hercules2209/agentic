import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.functions import available_functions, function_map
from functions.typeUnions import FunctionResponse
from config import MODEL_NAME, WORKING_DIR, MAX_ITERS
from prompts import SYSTEM_PROMPT
def generate_content(client: genai.Client, messages: List[types.Content],) ->FunctionResponse:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT,
            ),
        )
    except Exception as e:
        raise Exception(f"Error getting response: {e}")

    candidates:List[types.Candidate] = response.candidates or []
    
    metadata = response.usage_metadata
    
    text = response.text or ""
    function_calls = response.function_calls or []

    if metadata is None:
        return text, function_calls, candidates, 0, 0
    return text, function_calls, candidates, metadata.prompt_token_count, metadata.candidates_token_count


def run_agent_loop(client: genai.Client, messages: List[types.Content], verbose: bool = False,) -> None:
    response:str =""
    for iteration in range(1,MAX_ITERS+1): 
        if verbose:
            print(f"--- Iteration {iteration} ---")

        response, functions, candidates, prompt_tokens, response_tokens = generate_content(client, messages)
        
        for candidate in candidates:
            if candidate.content:
                messages.append(candidate.content)
        
        if functions:
            combined_parts:List[types.Part] = []
            for call in functions:
                tool_response = call_function(call, verbose)
                parts = tool_response.parts or []
                if not parts:
                    raise Exception(f"No parts returned from function call: {call.name}")
                part = parts[0]
                fr = part.function_response or None
                if fr is None or fr.response is None:
                    raise Exception(f"No response from function call: {call.name}")
                print(f"->function call response: {str(fr.response['result'])}")
                combined_parts.append(part)

            messages.append(types.Content(role="tool",parts=combined_parts))
            continue
        if not functions:
            print(f"AI: {response}")
        if verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            
        print("-" * 60, "\n")
        return

    print("⚠️ Reached max iterations without a final answer. Last LLM text:")
    print(response)

def call_function(function_call:types.FunctionCall, verbose:bool=False)->types.Content:
    try:
        function_name:str = function_call.name or ""
        if function_name =="":
            return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name = "",
                            response={"error":"Missing function name"}
                            )
                        ]
                    )

        args:Dict = function_call.args or {}
        args["working_directory"]=WORKING_DIR

        if verbose:
            print(f"Calling function: {function_name}({str(args)})")
        else:
            print(f" - Calling function: {function_name}")
        
        if not function_call.name in function_map.keys():
            return types.Content(
                    role = "tool",
                    parts=[
                        types.Part.from_function_response(
                            name = function_name,
                            response = {"error":f"Unknown function: {function_name}"},
                            )
                        ],
                    )
        try:
            function_response:str = function_map[function_name](**args)
        except Exception as e:
            return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name = function_name,
                            response = {"error": f"Execution error: {e}"}
                            )
                        ]
                    )
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response = {"result":function_response}
                        )
                    ]
            )
    except Exception as e:
        return types.Content(
                role="tool",
                parts=[
                        types.Part.from_function_response(
                            name = function_call.name or "",
                            response= {"error": f"Unknown error: {e}"}
                            )
                    ]
                )


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print('AI Code Assistant')
        print("Usage: python main.py \"<your prompt>\" [--verbose]")
        print("Error: Prompt not provided.")
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user",parts=[types.Part(text=user_prompt)])]
    try:
        run_agent_loop(client, messages, verbose)
    except Exception as e:
        print(f"Error generating response: {e}")
    sys.exit(0)

if __name__=="__main__":
    main()
