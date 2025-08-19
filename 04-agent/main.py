from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()
client = OpenAI()

def get_weather(city: str):
    return "42 degree c"


SYSTEM_PROMPT ="""
        You are an helpful AI assistant who specialized in resolving user query 
        You work on start, plan, action and observe mode

        For the given user query and available tools, plan the step by step execution, based on the planning,
        select the relevant tools from the available tools.
        based on the tools selection you have to perform an action to call the tool

        Wait for the observation and based on the observation from the tool call resolve the user query

        Rules:
            1. Follow the strict JSON output as per schema.
            2. Always perform one step at a time and wait for the next input.
            3. Carefully analyse the user query

        Output JSON Format:
        {{
            "step": "string",
            "content": "string",
            "function": "The name of function if the step is action",
            "input": "The input parameter for the function",
        }}
        
        Available Tools:
            -"get_weather": Takes the city name as an input and returns the current teperature for that city

        Example:
            User Query: What is the weather of new york?
            Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
            Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
            Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
            Output: {{ "step": "observe", "output": "12 Degree Cel" }}
            Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}


"""
messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
]

query = input("You:>")
messages.append({"role":"user","content":query})

while True:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type":"json_object"},
        messages=messages
    )
    messages.append({"role":"assistant", "content":response.choices[0].messsage.content})
    parsed_json= json.loads(response.choices[0].messsage.content)

    if parsed_json.get("step") =="plan":
        print(f"🧠:{parsed_json.get("content")}")
        continue

print(response.choices[0].message.content)