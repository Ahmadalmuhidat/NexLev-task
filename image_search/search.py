import os
import requests

from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def google_image_search(query: str, num = 1) -> list:
  try:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
      "q": query,
      "searchType": "image",
      "key": GOOGLE_API_KEY,
      "cx": GOOGLE_CSE_ID,
      "num": num
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()
    return [item["link"] for item in results.get("items", [])]

  except Exception as e:
    print(e)