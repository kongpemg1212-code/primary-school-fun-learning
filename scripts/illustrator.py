import os
import json
import requests
import time
from pathlib import Path
# No OpenAI import needed

def generate_image_free(prompt, filename):
    """
    Generates image using Pollinations.ai (Free, No Key)
    """
    try:
        # Construct prompt for kids style
        safe_prompt = f"cute cartoon {prompt} vector flat design minimalistic white background children book style"
        encoded_prompt = requests.utils.quote(safe_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={int(time.time())}&nologo=true"
        
        print(f"   🎨 Generating (Free AI): {prompt}...")
        
        # Download
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            output_dir = Path("assets/images")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Sanitize filename
            safe_filename = "".join([c for c in filename if c.isalnum() or c in (' ', '.', '_')]).strip()
            output_path = output_dir / safe_filename
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            return str(output_path), url
        else:
            print(f"❌ API Error {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Image generation failed for {prompt}: {e}")
        return None, None

def process_lesson(json_path):
    if not os.path.exists(json_path):
        print(f"❌ Input file not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Handle Chinese Vocabulary
    vocab_list = data.get('content', {}).get('vocabulary', [])
    updated_count = 0
    
    for item in vocab_list:
        word = item.get('word')
        definition = item.get('definition', '')
        
        # Check if image already exists
        if not item.get('image') or item.get('image') == "LEAVE_EMPTY_FOR_NOW":
            # Translate or use English word if available? 
            # Pollinations understands English better.
            # We assume 'word' might be Chinese. 
            # Simple heuristic: use definition if it looks English, or just word + definition
            search_term = f"{word} {definition}"
            
            local_path, url = generate_image_free(search_term, f"{word}.jpg")
            
            if local_path:
                item['image'] = local_path
                item['image_url'] = url 
                item['local_name'] = Path(local_path).name
                updated_count += 1
                print(f"✅ Saved to {local_path}")
            else:
                print(f"⚠️ Skipping image for {word}")
        else:
            print(f"ℹ️ Image already exists for {word}")
            
    # Handle Math Shapes (Optional: generate icon if missing?)
    # Math shapes are drawn by Canvas, so we might not need images.
    
    # Save updated JSON
    output_path = Path("temp") / "illustrated_lesson.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Illustrated data saved to {output_path} (Updated {updated_count} images)")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="temp/parsed_lesson.json", help="Input JSON path")
    args = parser.parse_args()
    
    process_lesson(args.input)
