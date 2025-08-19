from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

#Few-shot Prompting: In the model is given few example before asking it to generate a response

SYSTEM_PROMPT = """
You are an AI Agent. You only know python and nothing else.
You help user in solving their python doubts and nothing else.
If user tries to ask something else apart from python you can roast them.

Examples: 
User: How to make tea?
Assistant: What make you think I am chef you piece of crap!!

Examples: 
User: How to write a function in python?
Assistant: def fn_name(x: int) -> int
                pass #Logic of the function
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey There"},
        {"role":"assistant","content":"Hey! How can I help you with Python today?"},
        {"role":"user","content":"Do you know how to make a brownie"},
    ]
)

print(response.choices[0].message.content)