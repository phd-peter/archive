from google import genai
from google.genai import types
import os
import re
import json

def process_receipts(api_key):
    client = genai.Client(api_key=api_key)

    with open('demo-image.jpg', 'rb') as f:
        image_bytes = f.read()

    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents="Explain how AI works in a few words",
    #     config=types.GenerateContentConfig(
    #         thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    #     ),
    # )
    # print(response.text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            "Extract the paid amount(integer), date, and time from this image. Return the data in a JSON format. The JSON should be in the following format: {\"paid_amount\": \"100\", \"date\": \"2021-01-01\", \"time\": \"12:00:00\"}"
        ],
    )
    print(response.text)
    print("--------------------------------")
    raw = response.text.strip()
    # 코드블록 백틱이 있을 경우 제거
    if raw.startswith("```"):
        # Remove starting ``` or ```json and trailing ```
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL).strip()
    front_info = json.loads(raw)   # {'employee': '김익현', 'route': '회사-집'}
    print(front_info)

if __name__ == "__main__":
    process_receipts("AIzaSyCvoifyvGiq17O4a7cqr7RSiyZEdyp-VCc")