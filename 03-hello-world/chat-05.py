from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
SYSTEM_PROMPT ="""

"""
client = OpenAI()
query =input(":>")
messages =[
    {
        "role":"user","content":query
    }
]
response = client.chat.completions.create(
    model="gpt-4",
    response_format={"type":"json_object"},
    messages=messages
)