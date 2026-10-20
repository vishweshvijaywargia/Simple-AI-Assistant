from datetime import datetime
import os
import json
from utilities.utilities import log
import requests

def get_current_time () :
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_current_weather(city_name):
    url = f"https://wttr.in/{city_name}?format=3"
    resp = requests.get(url, timeout = 10)
    resp.raise_for_status()  # Raise an exception for HTTP errors
    return resp.text

def get_city() :
    return "Indore"

# def get_news_headlines():

#     url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=4871a74a66984e3c880618aa8247a6d6"

#     resp = requests.get(url, timeout=10)

#     data = resp.json()
#     headlines = []

#     for article in data.get("articles", []):
#         headlines.append({
#             "title": article.get("title")
#         })

#     return headlines

TOOLS =[{
    "type" : "function",
    "function" : {
        "name" : "get_current_time",
        "description" : "Returns the current date and time as a formatted string",
        "parameters" : {"type" : "object", "properties" : {}}
    } 
    }, 
    {
    "type" : "function",
    "function" : {
        "name" : "get_city_current_weather",
        "description" : "Returns the current weather for a given city",
        "parameters" :  {
            "type" : "object",
            "properties" :  {
                "city_name" : {"type" : "string", "description" : "The name of the city to get the weather for"}
                },
            "required" : ["city_name"]
            }
        }
    }, 
    {
    "type" : "function",
        "function" : {
            "name" : "get_city",
            "description" : "Returns the name of a city, whenever the user mentions for my city, my home, place where I live etc.",
            "parameters" : {"type" : "object", "properties" : {}}
        }
    }]
    # {
    # "type" : "function",
    # "function" : {
    #     "name" : "get_news_headlines",
    #     "description" : "Returns the latest news headlines for a usa",
    #     "parameters" : {
    #         "type" : "object",
    #         "properties" : {}
    #     }
    # }
    # }

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time" : get_current_time,
    "get_city_current_weather" : get_city_current_weather,
    "get_city" : get_city
    # "get_news_headlines" : get_news_headlines
}

def run_tool(tool_call):
    function_name = tool_call.function.name
    function_args = {}

    try:
        function_args = json.loads(tool_call.function.arguments or "{}") #convert string to dict, if no arguments, use empty dict
        func = FUNCTION_NAME_TO_FUNCTION_MAP.get(function_name)
        result = func(**function_args) if func else None #dictionary unpacking
    except Exception as e:
        result = f"Error executing tool '{function_name}': {str(e)}"

    log(f"Executing tool '{function_name}' with arguments: {function_args}")
    log(f"Tool '{function_name}' returned: {result}")
    return str(result)
