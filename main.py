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
    self.images_urls = []
  
  def search(self):
    try:
      self.images_urls.clear()
      search_query = analyze_query(self.search_entry.get())

      prompt = f"create an images search queries from based on this desc to get the best matches images: {search_query}"
      image_attributes = normal_message_to_open_ai(prompt).split("\n")

      for query in image_attributes:
        images_search_results = google_image_search(query)
        ranked_images = rank_images(
          images_search_results,
          json.loads(search_query)
        )
        for url, score in ranked_images:
          if score > 0.6:
            self.images_urls.append(url)
      
      self.display_images_results()

    except Exception as e:
      print(e)

  def display_images_results(self):
    try:
      for widget in self.result_frame.winfo_children():
        widget.destroy()

      for url in self.images_urls:
        response = requests.get(url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image = image.resize((400, 400))
        image = ImageTk.PhotoImage(image)

        label = customtkinter.CTkLabel(
          self.result_frame,
          image=image,
          text=""
        )
        # label.image = img
        label.pack(
          padx=10,
          pady=10
        )

    except Exception as e:
      print(e)

  def start(self):
    try:
      app = customtkinter.CTk()
      app.geometry("800x600")
      app.title("")

      self.search_entry = customtkinter.CTkEntry(
        app,
        placeholder_text="enter image description..."
      )
      self.search_entry.pack(
        pady=10,
        padx=10,
        fill="x"
      )

      load_button = customtkinter.CTkButton(
        app,
        text="search",
        command=self.search
        )
      load_button.pack(
        pady=10
      )

      scrollable_container = customtkinter.CTkScrollableFrame(
        app,
        orientation="vertical"
      )
      scrollable_container.pack(
        pady=10,
        padx=10,
        fill="both",
        expand=True
      )

      self.result_frame = scrollable_container

      app.mainloop()

    except Exception as e:
      print(e)

if __name__ == "__main__":
  program = Program()
  program.start()