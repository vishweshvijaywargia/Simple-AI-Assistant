from datetime import datetime
import os
import json
from utilities.utilities import log
import requests
from rag import search

def get_current_time () :
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_current_weather(city_name):
    url = f"https://wttr.in/{city_name}?format=3"
    resp = requests.get(url, timeout = 10)
    resp.raise_for_status()  # Raise an exception for HTTP errors
    return resp.text

def get_city() :
    return "Indore"

def get_news_headlines():

    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=4871a74a66984e3c880618aa8247a6d6"

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    headlines = []

    for article in data.get("articles", []):
        headlines.append({
            "News" : article.get("name"),
            "title": article.get("title")
        })

    return headlines

def search_knowledge_base(query):
    results = search(query, top_k=3)
    log(f"Search results for query '{query}'")

    for r in results:
        log(f"Score: {r['score']:.2f} - Source: {r['source']} # Chunk ID: {r['chunk_id']}")
    
    blocks = []

    for r in results:
        sourceFileName = r['source']
        chunkId = r['chunk_id']
        chunkText = r['text']

        header = f"Source: {sourceFileName} # Chunk ID: {chunkId}\n"
        block = f"{header}\n{chunkText}"
        blocks.append(block)

    return "\n\n".join(blocks)

TOOLS = [{
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
    }, 
    {
    "type" : "function",
    "function" : {
        "name" : "get_news_headlines",
        "description" : "Returns the latest news headlines when the user asks for news, latest news, news headlines, news updates etc.",
        "parameters" : {
            "type" : "object",
            "properties" : {}
        }
    } 
    }, 
    {
    "type" : "function",
    "function" : {
        "name" : "search_knowledge_base",
        "description" : "Searches the knowledge base for relevant information based on the user's query regarding the documents/policies of his/her organization that is Vijayvargiya & Associates",
        "parameters" : {
            "type" : "object",
            "properties" : {
                "query" : {"type" : "string", "description" : "The user's query to search in the knowledge base"}
            },
            "required" : ["query"]
        }
    }
    }]
    

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time" : get_current_time,
    "get_city_current_weather" : get_city_current_weather,
    "get_city" : get_city,
    "get_news_headlines" : get_news_headlines,
    "search_knowledge_base" : search_knowledge_base
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
