from dotenv import load_dotenv
import os
from openai import OpenAI
import json
load_dotenv()
# os.environ['PROMPT_FILE'] = 'prompts/baburao-prompt.txt'
# os.environ['PROMPT_FILE'] = 'prompts/hitesh-prompts.txt'
PROMPT_FILE = os.getenv('PROMPT_FILE')
client = OpenAI()
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
SYSTEM_PROMPT = load_prompt()
messages=[
        {
            "role": "system","content": SYSTEM_PROMPT
        }
    ]
print("Assistant is ready! Type your message below (type 'exit' to quit):")
while True:
    query =input("You> ")
    messages.append({"role":"user", "content":query})
    if query.strip().lower() in ["exit","goodbye","see you later","quit","bye"]:
        print("Exiting chat")
        break
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type":"json_object"},
        messages=messages
    )
    parsed_response = json.loads(response.choices[0].message.content)
    print("      🤖 ",parsed_response)
    messages.append({"role":"assistant","content":response.choices[0].message.content})
    if parsed_response.get('step') == "think":
        print("          🧠:", parsed_response.get('content'))
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        continue
    elif parsed_response.get('step')!= "result":
        print("     🧠",parsed_response.get('content'))
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        continue
    else:
        print("            ✅",parsed_response.get("content"))
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        
    