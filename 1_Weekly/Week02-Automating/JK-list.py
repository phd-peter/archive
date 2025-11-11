import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.helper_functions import print_llm_response, get_llm_response

print_llm_response("Hello, world!")
print(get_llm_response("Tell me a good joke."))

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather today?"}
]
print_llm_response(messages)

