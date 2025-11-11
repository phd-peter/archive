import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_llm_response(messages, model="o4-mini-2025-04-16"):
    """
    Calls the OpenAI API with the given messages and returns the response content.
    Args:
        messages (list or str): List of dicts with 'role' and 'content', or a string.
        model (str): Model name (default: o4-mini-2025-04-16).
    Returns:
        str: The assistant's reply.
    """
    if isinstance(messages, str):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": messages}
        ]
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content

def print_llm_response(messages, model="o4-mini-2025-04-16"):
    """
    Calls the OpenAI API and prints the response content.
    Args:
        messages (list or str): List of dicts with 'role' and 'content', or a string.
        model (str): Model name (default: o4-mini-2025-04-16).
    """
    response = get_llm_response(messages, model)
    print(response) 