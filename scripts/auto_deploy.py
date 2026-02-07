import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Add scripts directory to path to import modules
sys.path.append(str(Path(__file__).parent))

from smart_parser import parse_pdf, setup_gemini
from illustrator import process_lesson

def run_pipeline(pdf_path):
    print(f"🚀 Starting Auto Deploy Pipeline for: {pdf_path}")
    
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    temp_json = temp_dir / "parsed_lesson.json"
    
    # 1. Parse
    if not setup_gemini():
        print("⚠️ Gemini setup failed or no key found. Trying to skip parse if temp file exists.")
        
    data = parse_pdf(pdf_path)
    if not data:
        print("❌ Parse failed.")
        # Check if we have manual parsed data
        temp_json = Path("temp") / "parsed_lesson.json"
        if temp_json.exists():
            print("⚠️ Using existing parsed_lesson.json (Manual Override).")
            # Proceed
        else:
            return

    # Save temp (only if parse succeeded)
    if data:
        with open(temp_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    # 2. Illustrate
    # Note: process_lesson modifies file in place or writes to illustrated_lesson.json
    # My illustrator.py writes to illustrated_lesson.json
    process_lesson(str(temp_json))
    
    # Load illustrated data
    illustrated_json = temp_dir / "illustrated_lesson.json"
    if not illustrated_json.exists():
        # Fallback to parsed_lesson.json if illustrator failed
        print("⚠️ Illustration step skipped or failed. Using parsed data directly.")
        illustrated_json = temp_json
        
    with open(illustrated_json, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    # Normalize single object to list for batch processing
    if isinstance(new_data, dict):
        new_lessons_list = [new_data]
    else:
        new_lessons_list = new_data
        
    # 3. Update Data
    lessons_path = Path("data/lessons.json")
    if lessons_path.exists():
        with open(lessons_path, 'r', encoding='utf-8') as f:
            lessons = json.load(f)
    else:
        lessons = []
        
    # Assign ID
    max_id = max([l.get('id', 0) for l in lessons]) if lessons else 0
    
    # Check for duplicates based on title
    existing_titles = {l.get('title'): l.get('id') for l in lessons}
    
    updated_count = 0
    added_count = 0
    
    for new_lesson in new_lessons_list:
        new_title = new_lesson.get('title')
        
        if new_title in existing_titles:
            print(f"⚠️ Warning: Lesson '{new_title}' already exists (ID: {existing_titles[new_title]}).")
            # Update existing lesson instead of appending new one?
            target_id = existing_titles[new_title]
            new_lesson['id'] = target_id
            # Replace the old lesson with the new one
            for i, l in enumerate(lessons):
                if l.get('id') == target_id:
                    lessons[i] = new_lesson
                    break
            print(f"🔄 Updated existing lesson (ID: {target_id})")
            updated_count += 1
        else:
            max_id += 1
            new_lesson['id'] = max_id
            lessons.append(new_lesson)
            print(f"✅ Added new lesson '{new_title}' (ID: {new_lesson['id']})")
            added_count += 1
    
    print(f"📊 Summary: {added_count} added, {updated_count} updated.")
    
    with open(lessons_path, 'w', encoding='utf-8') as f:
        json.dump(lessons, f, indent=2, ensure_ascii=False)
    print(f"✅ Updated lessons.json with new lesson (ID: {new_lesson['id']})")
    
    # 4. Deploy (Git)
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"feat: add new lesson {new_lesson.get('title', 'Unknown')}"], check=True)
        # Check remote before push
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        if "origin" in result.stdout:
            subprocess.run(["git", "push"], check=True)
            print("✅ Deployed successfully! Check GitHub Pages.")
        else:
            print("⚠️ No remote 'origin' found. Skipping push.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git deploy failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path", help="Path to PDF file")
    args = parser.parse_args()
    
    run_pipeline(args.pdf_path)
