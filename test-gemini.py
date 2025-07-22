from google import genai
from google.genai import types
import os

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyCvoifyvGiq17O4a7cqr7RSiyZEdyp-VCc")


def extract_front(image_path: str) -> str:
    """Extract the paid amount (integer), date, and time from the front page of a receipt.

    Args:
        image_path (str): Path to the front image.

    Returns:
        str: JSON string with keys "paid_amount", "date", and "time".
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            (
                "Extract the paid amount(integer), date, and time from this image. "
                "Return the data in a JSON format. The JSON should be in the following format: "
                '{"paid_amount": "100", "date": "2021-01-01", "time": "12:00:00"}'
            ),
        ],
    )
    return response.text


def extract_back(image_path: str) -> str:
    """Extract the date, name, and route from the back page of a receipt.

    Args:
        image_path (str): Path to the back image.

    Returns:
        str: JSON string with keys "date", "name", and "route".
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            (
                """Extract the date, name, route from this image. Return the data in a JSON format. name은 "최홍영", "박다혜", "박상현", "김민주", "최윤선", "김익현", "장수현", "이한울", "김호연", "박성진" 중 하나이다.
                The JSON should be in the following format: {\"date\": \"MM-DD\", \"name\": \"김익현\", \"route\": \"회사->집\"}"""
            ),
        ],
    )
    return response.text


def process_receipts(img_dir: str = "img") -> None:
    """Pair images in `img_dir` alphabetically and process them using the extractor functions.

    Assumes the files are ordered as: front1, back1, front2, back2, ... etc.
    """
    # Collect image files and sort alphabetically.
    files = sorted(
        [f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    )

    if len(files) % 2 != 0:
        print("⚠️  The number of images is odd; the last image will be skipped.")

    for i in range(0, len(files) - 1, 2):
        front_path = os.path.join(img_dir, files[i])
        back_path = os.path.join(img_dir, files[i + 1])

        front_result = extract_front(front_path)
        back_result = extract_back(back_path)

        receipt_idx = (i // 2) + 1
        print(f"===== Receipt {receipt_idx} =====")
        print("Front:", front_result)
        print("Back :", back_result)
        print()


if __name__ == "__main__":
    # Default to processing the built-in `img` directory relative to this script.
    process_receipts()