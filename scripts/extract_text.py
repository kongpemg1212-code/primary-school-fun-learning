import fitz  # PyMuPDF
import json

doc = fitz.open("primary-school-fun-learning/语文一年级下册（2025春）.pdf")

for i in range(25): # Pages 0-24 (Unit 1: Literacy)
    try:
        page = doc[i]
        text = page.get_text("text")
        print(f"--- Page {i+1} ---\n{text}\n")
    except Exception:
        pass
