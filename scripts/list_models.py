import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Setup (Try ADC)
try:
    if os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    else:
        # Implicit ADC
        pass
        
    print("🔍 Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"📝 Text/Multi: {m.name}")
        if 'generateImage' in m.supported_generation_methods or 'image' in m.name.lower():
            print(f"🎨 Image:      {m.name}")
            
except Exception as e:
    print(f"❌ Error: {e}")
