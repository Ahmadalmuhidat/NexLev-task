import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0)

def normal_message_to_open_ai(prompt: str):
  try: 
    return llm.invoke([HumanMessage(content=prompt)]).content

  except Exception as e:
    print(e)

def analyze_query(description: str) -> str:
  try:
    system_message = SystemMessage(
      content='''You are an assistant that breaks down complex image descriptions into components like:
      people, objects, actions, background, and location.
      '''
    )
    human_message = HumanMessage(content=f"Break down this image description: {description}. Return the result in JSON format.")
    return llm.invoke([system_message, human_message]).content

  except Exception as e:
    print(e)