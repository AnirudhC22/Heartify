from google import genai
from google.genai import types


def generate(text):

    client = genai.Client(api_key="AIzaSyDYFh1e7nNeZgXwYEIZYjMvuMSnjalexnI")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"Explain how {text} works"],
        config=types.GenerateContentConfig(
            max_output_tokens=100,
            temperature=0.1
        )
    )
    return response.text

print(generate("car"))


