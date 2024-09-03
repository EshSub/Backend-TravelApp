"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import json
import environ
import google.generativeai as genai


env = environ.Env()

environ.Env.read_env()
# gemini_api_key = env("GEMINI_API_KEY")

genai.configure(api_key="AIzaSyDJh_yYbR-2LzxMvyhM03h90qXHdooGTN8")

def get_plan(duration=7, preferred_activities=["diving", "snorkelling", "kayaking", "sea bathing", "boat rides"], description="I want to do some water activities around downsouth area"):
    
  # Create the model
  # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
  generation_config = {
    "temperature": 0.55,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    # "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )


  day = 1
  prevloc = set()
  final_location = "Colombo"
  duration = 5
  # preferred_activities = ["diving", "snorkelling", "kayaking", "sea bathing", "boat rides"]
  preferred_activities = ["animals"]
  description = "I like anything to do with animals"

  chat = model.start_chat(history=[])

  plans_per_day = []
  for i in range(1, duration+1):
    
    response = chat.send_message([
    """input: I am on a trip to Sri Lanka. This is day {i}. Give me a trip plan for today based on the User Inputs. First identify a pattern of my intrest using the preffered activities and the description and find unique activities for me to do each day checking the previous activities done covering most areas of Sri Lanka. Please take care to give the area as a district of Sri Lanka. Strictly adhere to the given output format of JSON string.
    User Input: \n {general: {Previous locations :[ ]} , Last location: Colombo , preferred_activities: [diving, snorkelling,kayaking, sea bathing, boat rides] , description: "I want to do some water activities around downsouth area"}"""	,
    """output:
    [
    {
      "type": "food",
      "time": "morning",
      "area": "Galle",
      "props": {
        "food": "breakfast",
        "type": "traditional",
        "price": "low"
      }
    },
    {
      "type": "destination",
      "time": "morning",
      "area": "Galle",
      "activities": "surfing",
      "props": {
        "type": "adventure",
        "price": "medium"
      }
    },
    {
      "type": "food",
      "time": "evening",
      "area": "Galle",
      "props": {
        "food": "lunch",
        "type": "traditional",
        "price": "low"
      }
    },
    {
      "type": "destination",
      "time": "afternoon",
      "area": "Galle",
      "activities": "kayaking",
      "props": {
        "type": "adventure",
        "price": "medium"
      }
    },
    {
      "type": "food",
      "time": "night",
      "area": "Galle",
      "props": {
        "food": "dinner",
        "type": "seafood",
        "price": "medium"
      }
    },
    {
      "type": "accommodation",
      "time": "night",
      "area": "Galle",
      "props": {
        "type": "hotel",
        "price": "medium"
      }
    }
  ]""",
    f"""input: I am on a trip to Sri Lanka. This is day {i}. Give me a trip plan for today based on the User Inputs. First identify a pattern of my intrest using the preffered activities and the description and find unique activities for me to do each day checking the previous activities done covering most areas of Sri Lanka. Strictly adhere to the given output format of JSON string.
    User Input: \n Previous locations : {prevloc} , Last location: {final_location} , preferred_activities: {preferred_activities} , description: "{description}" 
    """,
    "output:",
    ])
    # print('```' == response.text[-3:])
    # print(response.text)
    try:
      final_response = json.loads(response.text.strip()[8:-3])
    except Exception as e:
      return response.text,"FAILED"
    final_location = final_response[-1]['area']
    for item in final_response:
      if item['type'] == 'destination':
        prevloc.add(item['area']+" "+item['activities'])

    plans_per_day.append(final_response)
    # print(final_response)
    # print(final_location)
    # print(prevloc)
    # # print(response.text)

  return plans_per_day, "SUCCESS"

def chat_ai_response(history):
    if not history:
        return "No message received."
    
    generation_config = {
        "temperature": 0.55,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        # "response_mime_type": "text/plain",
    }

    # Initialize the model with the specified configuration and safety settings
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings=safety_settings
    )

    # Start a chat session using the model
    chat_session = model.start_chat()

    # Sending the most recent message in history to the model
    response = chat_session.send_message(history)
    return response.text

def chat_ai_response1(history):
    if not history:
        return "No message received."
    
    generation_config = {
        "temperature": 0.55,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        # Ensure this field is valid or remove it if causing issues
        # "response_mime_type": "text/plain",
    }

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        chat_session = model.start_chat()
        response = chat_session.send_message(f"Give the answer to the first question: {history[0]}, If possible try to get context from other questions and answers in this list {history}. Only give the answer to the first question, nothing else.")
        return response.text
    except Exception as e:
        print("An error occurred:", e)
        return "An error occurred while generating the response."

if __name__ == "__main__":
    plans, status = get_plan()
    print(plans, status)
    # print(chat_ai_response(["Hello", "How are you?"]))
    # print(chat_ai_response1(["Hello", "How are you?"]))