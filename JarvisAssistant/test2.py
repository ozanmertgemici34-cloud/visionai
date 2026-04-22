import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing API Key starting with: {api_key[:10]}...")

genai.configure(api_key=api_key)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            
    print("-------------------")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Merhaba!")
    print("SUCCESS 1.5-flash: ", response.text)
except Exception as e:
    print("ERROR:", e)
