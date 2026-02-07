import os
import json
import requests
import time
from pathlib import Path

def generate_image_free(prompt, filename):
    """
    Generates image URL using Lorem Flickr (Reliable, Free)
    """
    try:
        # Simple keyword extraction (first 1-2 words)
        keywords = prompt.split(' ')[0]
        if len(keywords) < 3: 
             parts = prompt.split(' ')
             if len(parts) > 1:
                 keywords = parts[1]
        
        keywords = "".join([c for c in keywords if c.isalnum()])
        # Use cartoon/cat as fallback category to make it fun for kids
        url = f"https://loremflickr.com/512/512/{keywords},cartoon/all"
        
        print(f"   🎨 Using Lorem Flickr: {keywords}...")
        
        response = requests.get(url, timeout=30, allow_redirects=True)
        if response.status_code == 200:
            output_dir = Path("assets/images")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            safe_filename = "".join([c for c in filename if c.isalnum() or c in (' ', '.', '_')]).strip()
            output_path = output_dir / safe_filename
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return str(output_path), url
        else:
            return None, None
            
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None, None

def process_lesson(json_path):
    if not os.path.exists(json_path):
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if isinstance(data, list):
        lessons = data
    else:
        lessons = [data]
        
    for lesson in lessons:
        vocab_list = lesson.get('content', {}).get('vocabulary', [])
        for item in vocab_list:
            word = item.get('word')
            definition = item.get('definition', '')
            
            # Check exist (Relative path!)
            if (Path("assets/images") / f"{word}.jpg").exists():
                print(f"ℹ️ Exists: {word}")
                item['image'] = f"assets/images/{word}.jpg"
                continue
                
            # Generate
            search_term = definition if definition else word
            local_path, url = generate_image_free(search_term, f"{word}.jpg")
            
            if local_path:
                item['image'] = str(local_path)
                item['image_url'] = url
                print(f"✅ Saved: {local_path}")
            else:
                # Fallback to text placeholder
                item['image'] = "" 

    # Save
    output_path = Path("temp") / "illustrated_lesson.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="temp/parsed_lesson.json", help="Input JSON path")
    args = parser.parse_args()
    
    process_lesson(args.input)
