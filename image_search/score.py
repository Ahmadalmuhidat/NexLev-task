import requests
import json

from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel

def extract_attributes(attributes):
  try:
    if isinstance(attributes, str):
      attributes = json.loads(attributes)

    character_desc = attributes.get("people", [""])[0]
    action_desc = ", ".join(attributes.get("actions", []))
    background_desc = attributes.get("background", [""])[0]
    location_desc = attributes.get("location", [""])[0]
    return character_desc, action_desc, background_desc, location_desc

  except Exception as e:
    print(e)

def get_image_score(image_url: str, attributes: dict) -> float:
  try:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    weights = {
      "character": 0.4,
      "action": 0.2,
      "background": 0.2,
      "location": 0.2
    }

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")

    character_desc, action_desc, background_desc, location_desc = extract_attributes(attributes)

    parts = {
      "character": character_desc,
      "action": action_desc,
      "background": background_desc,
      "location": location_desc
    }

    total_score = 0.0
    for key, desc in parts.items():
      if not desc:
        continue
      # Always compare against a neutral or unrelated caption
      text_prompts = [desc, "A completely unrelated image"]
      inputs = processor(text=text_prompts, images=image, return_tensors="pt", padding=True)
      outputs = model(**inputs)
      logits_per_image = outputs.logits_per_image
      probs = logits_per_image.softmax(dim=1)
      score = probs[0][0].item()
      total_score += score * weights[key]
    
    return round(total_score, 4)

  except Exception as e:
    print("Error:", e)
    return 0.0

def rank_images(images: list, desc_analyze: str) -> list:
  try:
    scored_images = []
    for img in images:
      score = get_image_score(img, desc_analyze)
      scored_images.append((img, score))

    scored_images.sort(key=lambda x: x[1], reverse=True)
    return scored_images

  except Exception as e:
    print(e)
