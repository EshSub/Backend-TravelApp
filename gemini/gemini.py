"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import json

import google.generativeai as genai
from gemini.gemini_config import gemini_api_key

genai.configure(api_key=gemini_api_key)

def get_plan(duration=7, preferred_activities=["diving", "snorkelling", "kayaking", "sea bathing", "boat rides"], description="I want to do some water activities around downsouth area"):
    
  # Create the model
  # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
  generation_config = {
    "temperature": 0.55,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
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