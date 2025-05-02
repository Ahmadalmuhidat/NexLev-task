import json

from image_search.langchain import analyze_query, normal_message_to_open_ai
from image_search.search import google_image_search
from image_search.score import rank_images

if __name__ == "__main__":
  desc = input("enter image desc: ")
  desc_analyze = analyze_query(desc)

  image_search_queries = normal_message_to_open_ai("create an images search queries from based on this desc to get the best matches images: " + desc_analyze).split("\n")

  for query in image_search_queries:
    images_urls = google_image_search(query)
    ranked_images = rank_images(images_urls, json.loads(desc_analyze))
    for url, score in ranked_images:
      print(f"- {url} (Score: {score})")