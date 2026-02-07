import os
import json
import time
import argparse
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (optional for ADC)
load_dotenv()

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("🔑 Using GEMINI_API_KEY from environment.")
        genai.configure(api_key=api_key)
    else:
        print("🌐 No API Key found. Attempting to use Application Default Credentials (ADC)...")
        # In Google Cloud environment or local with gcloud auth, this works automatically.
        try:
            # Check if default credentials work by listing models (lightweight check)
            # Or just proceed, library handles it.
            pass 
        except Exception as e:
            print(f"⚠️ ADC Warning: {e}")
    return True

def parse_pdf(pdf_path):
    print(f"🚀 Starting parse for: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return None

    # Upload file
    print("📤 Uploading PDF to Gemini...")
    try:
        sample_file = genai.upload_file(path=pdf_path, display_name="Lesson PDF")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print("💡 Hint: Ensure you have run 'gcloud auth application-default login' or set GEMINI_API_KEY.")
        return None
    
    # Wait for processing
    print(f"⏳ Waiting for processing... State: {sample_file.state.name}")
    while sample_file.state.name == "PROCESSING":
        time.sleep(2)
        sample_file = genai.get_file(sample_file.name)
        print(f"   State: {sample_file.state.name}")
        
    if sample_file.state.name == "FAILED":
        print("❌ File processing failed.")
        return None

    print("✅ File processed. Generating content with Gemini 3.0 Pro...")

    # Try Gemini 3.0 Pro first, fallback if needed
    model_name = "gemini-3.0-pro" # Assumed standard name
    
    try:
        model = genai.GenerativeModel(model_name)
    except Exception:
        print(f"⚠️ Model '{model_name}' not found. Trying 'gemini-1.5-pro'...")
        model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = """
    You are an expert primary school education assistant. 
    Analyze this PDF (which is a Chinese or Math lesson textbook page).
    Extract the content into a structured JSON format suitable for the learning app.

    The JSON structure must match this example:
    {
        "subject": "Chinese",  // or "Math"
        "title": "Lesson Title",
        "content": {
            "subject": "语文", // or "数学"
            "title": "Lesson Title",
            "category": "Category (e.g. 识字, 古诗)",
            "vocabulary": [
                {
                    "word": "Word",
                    "pinyin": "pinyin",
                    "definition": "Simple definition",
                    "example": "Simple example sentence",
                    "image_url": "" 
                }
            ],
            "sentences": [
                "Sentence 1",
                "Sentence 2"
            ],
            "shapes": [] // Only for Math: list of {type: "rectangle/square/triangle/circle", name, desc}
        }
    }
    
    Rules:
    1. If it's a Chinese lesson, extract vocabulary (生字/词语) and key sentences/poems.
    2. If it's a Math lesson, extract shapes or key concepts.
    3. Return ONLY valid JSON, no markdown formatting like ```json.
    """

    try:
        response = model.generate_content([prompt, sample_file])
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        if "404" in str(e):
             print(f"💡 Hint: Model {model_name} might not be available in your region or project.")
        return None
    
    # Cleanup
    print("🧹 Deleting remote file...")
    try:
        sample_file.delete()
    except:
        pass
    
    try:
        # Strip markdown if present
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"): # In case it's just ```
             text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"❌ JSON Parse Error: {e}")
        print("Raw response:", response.text)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to PDF file")
    args = parser.parse_args()
    
    if setup_gemini():
        data = parse_pdf(args.pdf_path)
        
        if data:
            output_dir = Path("temp")
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / "parsed_lesson.json"
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to {output_path}")
