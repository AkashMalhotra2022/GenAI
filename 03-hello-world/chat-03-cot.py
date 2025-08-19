from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()
#chain of Thought: The model is encouraged to breakdown reasoning step by step before arriving to a solution
SYSTEM_PROMPT ="""
            You are an helpful AI assistant who is speciazlized in resolving user query.
            For the given user input, analyse the input and break down the problem step by step.
            The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation. 
            Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".
            Rules:
            1. Follow the strict JSON output as per schema.
            2. Always perform one step at a time and wait for the next input.
            3. Carefully analyse the user query,
            Output Format:
            {{ "step": "string", "content": "string" }}
"""
client = OpenAI()
messages=[
        {
            "role": "system","content": SYSTEM_PROMPT
        }
    ]
query =input("> ")
messages.append({"role":"user", "content":query})
while True:
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type":"json_object"},
        messages=messages
    )
    parsed_response = json.loads(response.choices[0].message.content)
    print("      🤖 ",parsed_response)
    messages.append({"role":"assistant","content":response.choices[0].message.content})
    if parsed_response.get('step')!= "result":
        print("     🧠",parsed_response.get('content'))
        continue
    print("            ✅",parsed_response.get("content"))
    break
    