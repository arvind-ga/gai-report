import os
import numpy as np
import time
from datetime import datetime
import requests


# from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

### azure configuration
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
print("API_KEY:", API_KEY)
print("ENDPOINT:", ENDPOINT)

###################
# pers_prompt = """
#   # YOUR ROLE #
#   You are a career counsellor expert. Summerize us about student's personality in a paragraph based on
#   below personality distribution.

#   # STUDENT RESPONSE #
#   student's personality distribution{pers_dict}
#   """

# apti_prompt = """
#   # YOUR ROLE #
#   You are a career counsellor expert. Summerize us about student's aptitude prformance base on the
#   aptitude performance dictionary.

#   # STUDENT RESPONSE #
#   student's personality distribution{apti_dict}
#   """


###### Azure AI
def gpt4_pers_response(prompt1):

    content = prompt1
    ###################

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": content,
                        # "text": "You are an AI assistant that helps people find information."
                    }
                ],
            }
        ],
        "temperature": 0.5,
        "top_p": 0.15,
        "max_tokens": 800,
    }

    ### Model Out
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        # response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        # print(
        #     "GPT4 RESPONSE::::::",
        #     response.get("choices")[0].get("message").get("content"),
        # )
        return response
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
