from datetime import datetime
import os
import requests
def get_current_time () :
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_current_weather(city_name):
    url = f"https://wttr.in/{city_name}?format=3"
    resp = requests.get(url, timeout = 10)
    if resp.status_code != 200:
        return f"Failed to fetch weather data for {city_name}. Please try again later."
    return resp.text

def get_news_headlines():

    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=4871a74a66984e3c880618aa8247a6d6"

    resp = requests.get(url, timeout=10)

    if resp.status_code == 200:
        data = resp.json()
        headlines = []

        for article in data.get("articles", []):
            headlines.append({
                "title": article.get("title", "No title")
            })

        return headlines

    return f"Failed to fetch news: {resp.status_code} - {resp.text}"

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
        "name" : "get_news_headlines",
        "description" : "Returns the latest news headlines for a usa",
        "parameters" : {
            "type" : "object",
            "properties" : {}
        }
    }
    }]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time" : get_current_time,
    "get_city_current_weather" : get_city_current_weather,
    "get_news_headlines" : get_news_headlines
}