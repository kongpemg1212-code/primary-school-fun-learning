import fitz  # PyMuPDF
import json

doc = fitz.open("primary-school-fun-learning/1年级下册（2025春）_Part1_P1-33.pdf")
page = doc[7] # Page 8 (index 7)
text = page.get_text("text")

print(f"--- Page 5 Content ---\n{text}\n----------------------")

# Quick manual JSON construction for demo if text is good
data = {
    "subject": "Chinese",
    "title": "Spring", # Placeholder
    "content": {
        "subject": "语文",
        "title": "Sample Lesson",
        "category": "识字",
        "vocabulary": [],
        "sentences": []
    }
}
with open("primary-school-fun-learning/temp/parsed_lesson.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
