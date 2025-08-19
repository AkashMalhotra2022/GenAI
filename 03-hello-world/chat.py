from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

#Zero-shot Prompting: In this model is given direct question or task

SYSTEM_PROMPT = """
You are an AI Agent. You only know python and nothing else.
You help user in solving their python doubts and nothing else.
If user tries to ask something else apart from python you can roast them.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey There"},
        {"role":"assistant","content":"Hey! How can I help you with Python today?"},
        {"role":"user","content":"Do you know how to make tea without adding milk?"},
    ]
)

print(response.choices[0].message.content)