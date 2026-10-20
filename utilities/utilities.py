import os
def log(text):
    if os.getenv("DEBUG") == "True":
        print(f" \033[90m{text}\033[0m")  # Print in gray color for debug messages