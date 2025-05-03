i have developed desktop app with customtkinter that lets users search for images by typing a description.

1. User enters a description.
2. The app uses AI (OpenAI + LangChain) to understand and improve that description.
3. It then generates multiple image search queries and uses Google image search to find results.
4. The results are ranked based on how well they match the original description.
5. Only the top images (with a score > 0.6) are shown in the app.
6. Each image is downloaded and displayed in a scrollable window inside the app.

I have used OpenAI's CLIP model to score how well an image matches certain descriptions. CLIP understands both text and images, and tells us how closely they match.

1. How it works:
  We break down the image description into 4 parts (Character, Action, Background, Location)
2. Each part is given a weight (e.g., character is most important at 40%).
3. For each part:
  We give CLIP two texts, the real description (e.g., "a man riding a horse") and a dummy unrelated one.
  CLIP checks how closely the image matches the correct one vs. the dummy.
  It gives a probability score (closer to 1 means better match).
4. Each score is multiplied by its weight and added up to get a final score between 0 and 1.
5. This score helps us rank the images and show only the most relevant ones.


Note: only the images that have scores +0.6 will be displayed in the result page.
Note: some search queries might return errors from the google images search api.