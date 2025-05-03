import requests
import json

from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel

def extract_attributes(attributes: str):
  try:
    if isinstance(attributes, str):
      attributes = json.loads(attributes)

    character_description = attributes.get("people", [""])[0]
    action_description = ", ".join(attributes.get("actions", []))
    background_description = attributes.get("background", [""])[0]
    location_description = attributes.get("location", [""])[0]

    return character_description, action_description, background_description, location_description

  except Exception as e:
    print(e)

def get_image_score(image_url: str, image_attributes: dict) -> float:
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

    character_description, action_description, background_description, location_description = extract_attributes(image_attributes)

    parts = {
      "character": character_description,
      "action": action_description,
      "background": background_description,
      "location": location_description
    }

    total_score = 0.0
    for key, desc in parts.items():
      if not desc:
        continue
      text_prompts = [desc, "a completely unrelated image"]
      inputs = processor(text=text_prompts, images=image, return_tensors="pt", padding=True)
      outputs = model(**inputs)
      logits_per_image = outputs.logits_per_image
      probs = logits_per_image.softmax(dim=1)
      score = probs[0][0].item()
      total_score += score * weights[key]
    
    return round(total_score, 4)

  except Exception as e:
    print(e)
    return 0.0

def rank_images(images: list, image_attributes: str) -> list:
  try:
    scored_images = []
    for image in images:
      score = get_image_score(image, image_attributes)
      scored_images.append((image, score))

    scored_images.sort(key=lambda x: x[1], reverse=True)
    return scored_images

  except Exception as e:
    print(e)
