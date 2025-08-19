import os
from dotenv import load_dotenv
from clients import get_openai_client

load_dotenv()

OPENAI_MODEL = os.getenv('OPENAI_MODEL')
PROMPT_FILE = os.getenv('PROMPT_FILE')

def load_prompt():
    """
    Loads the prompt content from the file path specified in the PROMPT_FILE environment variable.
    Supports .txt (plain text) and .py (Python file with a variable named 'prompt' or ending with '_prompt').
    """
    if not PROMPT_FILE:
        raise Exception("PROMPT_FILE environment variable not set.")

    prompt_path = os.path.join(os.path.dirname(__file__), PROMPT_FILE)
    if not os.path.exists(prompt_path):
        raise Exception(f"Prompt file '{PROMPT_FILE}' not found at '{prompt_path}'.")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt = f.read()
        print(f"Loaded prompt: {prompt}")
        return prompt
    
    
    
def get_response(messages):
        client = get_openai_client()
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI Error: {e}")
    
        except Exception as e:
            raise RuntimeError(f"Gemini Error: {e}")
    
    