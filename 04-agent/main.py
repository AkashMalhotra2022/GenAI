from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import requests
import os
load_dotenv()
client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"


available_tools ={
    "get_weather": get_weather,
    "run_command": run_command
}


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
            - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.

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
while True:
    query = input("You:>")
    messages.append({"role":"user","content":query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type":"json_object"},
            messages=messages
        )
        messages.append({"role":"assistant", "content": response.choices[0].message.content})
        parsed_json= json.loads(response.choices[0].message.content)

        if parsed_json.get("step") =="plan":
            print(f"🧠:{parsed_json.get("content")}")
            continue
        if parsed_json.get("step")=="action":
            tool_function = parsed_json.get("function")
            tool_input = parsed_json.get("input")

            print(f"🛠️:Calling Tool:{tool_function} with input {tool_input}")

            if available_tools.get(tool_function)!= False:
                output = available_tools[tool_function](tool_input)
                messages.append({"role":"user","content":json.dumps({"step":"observe","output":output})})
                continue
        if parsed_json.get("step")=="output":
            print(f"✅: {parsed_json.get("content")}")



# print(response.choices[0].message.content)