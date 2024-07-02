"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai
import gemini.gemini_config as gemini_config

genai.configure(api_key=gemini_config.gemini_api_key)

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

response = model.generate_content([
  "input: A trip plan needs to be based on the following user input. First, go over the general details. Then refine the options based on the day-by-day information provided by the user. Finally, format the output in the required format provided in the example.\n\nUser Input:\n{  general: {    country: \"Sri Lanka\", duration: 1,    preferred_activities: [      \"surfing\",      \"hiking\",        \"swimming\",  \"trekking\"   ],    food: [      \"any\",    ],    budget: [\"medium\"],    activity_hardness_level: [\"low\"],    duration: [\"medium\"],    description: \"I want to go on a trip to the south and enjoy the beaches. I want to eat seafood and have a medium budget. I want to go for 1 day.\"  },  daily_preferences: [    {      date_range: { start: 1, end: 1},      activities: [\"cycling\", \"surfing\",\"swimming\"],      food: [\"any\"],      budget: \"low\",      activity_hardness_level: \"high\",      duration: \"short\",    },  ],};",
  "output: [  {    type: \"destination\",    time: \"morning\",    area: \"rumassala\",    activities: [\"snorkeling\", \"jungle trekking\", \"beach\"],    props: {      type: \"adventure\",      price: \"free\",    },  },  {    type: \"food\",    time: \"morning\",    area: \"rumassala\",    props: {      food: \"breakfast\",      type: \"local\",      price: \"low\",    },  },  {    type: \"travel\",    time: \"morning\",    props: {      confortable: \"yes\",      price: \"low\",      start: \"rumassala\",      end: \"galle\",    },  },  {    type: \"destination\",    time: \"evening\",    area: \"galle\",    props: {      type: \"cultural\",      price: \"free\",    },  },  {    type: \"food\",    time: \"evening\",    area: \"galle\",    props: {      food: \"dinner\",      type: \"local\",      price: \"low\",    },  },  {    type: \"travel\",    time: \"evening\",    props: {      confortable: \"yes\",      price: \"low\",      start: \"galle\",      end: \"unawatuna\",    },  },  {    type: \"destination\",    time: \"night\",    area: \"unawatuna\",    props: {      type: \"beach\",      price: \"free\",    },  },  {    type: \"food\",    time: \"night\",    area: \"unawatuna\",    props: {      food: \"dinner\",      type: \"local\",      price: \"low\",    },  },  {    type: \"accommodation\",    time: \"night\",    area: \"unawatuna\",    props: {      type: \"hotel\",      price: \"low\",    },  },];",
  "input: A trip plan needs to be based on the following user input. First, go over the general details. Then refine the options based on the day-by-day information provided by the user. Finally, format the output in the required format provided in the example.\n\n\
    User Input:\n{  general: {    country: \"Sri Lanka\", duration: 6,    preferred_activities: [      \"surfing\",      \"hiking\",        \"swimming\",  \"snorkelling\"  ],    food: [      \"any\",    ],    budget: [\"medium\"],    activity_hardness_level: [\"low\"],    duration: [\"medium\"],    description: \"I want to go on a trip to the mountains and do some hiking. I want to eat seafood and have a medium budget. I want to go for 4 days.\"  },  daily_preferences: [    {      date_range: { start: 1, end: 2 },      activities: [\"cycling\", \"surfing\"],      food: [\"pizza\", \"burgers\"],      budget: \"low\",      activity_hardness_level: \"high\",      duration: \"short\",    },    {      date_range: { start: 2, end: 4 },      activities: [\"hiking\"],      food: [\"any\"],      budget: \"medium\",      activity_hardness_level: \"medium\",    },    {      date_range: { start: 4, end: 6 },      activities: [\"kayaking\"],      food: [\"rice\", \"pasta\"],      budget: \"high\",      activity_hardness_level: \"medium\",    },  ],};",
  "output: ",
])

print(response.text)