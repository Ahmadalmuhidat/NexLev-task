import json
import requests
import customtkinter

from PIL import Image, ImageTk
from io import BytesIO
from image_search.langchain import analyze_query, normal_message_to_open_ai
from image_search.search import google_image_search
from image_search.score import rank_images

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class Program:
  def __init__(self):
    self.image_urls = []
  
  def search(self):
    try:
      self.image_urls.clear()
      desc_analyze = analyze_query(self.search_entry.get())

      prompt = f"create an images search queries from based on this desc to get the best matches images: {desc_analyze}"
      image_search_queries = normal_message_to_open_ai(prompt).split("\n")

      for query in image_search_queries:
        images_urls = google_image_search(query)
        ranked_images = rank_images(images_urls, json.loads(desc_analyze))
        for url, score in ranked_images:
          if score > 0.6:
            self.image_urls.append(url)
            print(f"- {url} (Score: {score})")
      
      self.display_images()

    except Exception as e:
      print(e)

  def display_images(self):
    try:
      for widget in self.result_frame.winfo_children():
        widget.destroy()

      for url in self.image_urls:
        response = requests.get(url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((400, 400))
        img = ImageTk.PhotoImage(img)

        label = customtkinter.CTkLabel(self.result_frame, image=img, text="")
        # label.image = img
        label.pack(padx=10, pady=10)

    except Exception as e:
      print(e)

  def start(self):
    try:
      app = customtkinter.CTk()
      app.geometry("800x600")
      app.title("Display Images from URL Array")

      self.search_entry = customtkinter.CTkEntry(app, placeholder_text="Enter something if you want...")
      self.search_entry.pack(pady=10, padx=10, fill="x")

      load_button = customtkinter.CTkButton(app, text="Load Images", command=self.search)
      load_button.pack(pady=10)

      scrollable_container = customtkinter.CTkScrollableFrame(app, orientation="vertical")
      scrollable_container.pack(pady=10, padx=10, fill="both", expand=True)

      self.result_frame = scrollable_container

      app.mainloop()

    except Exception as e:
      print(e)

if __name__ == "__main__":
  program = Program()
  program.start()