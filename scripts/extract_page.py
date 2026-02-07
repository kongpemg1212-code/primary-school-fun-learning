from pdf2image import convert_from_path
import os

# Create temp dir
os.makedirs("primary-school-fun-learning/temp", exist_ok=True)

# Convert page 5 (index 4)
images = convert_from_path('primary-school-fun-learning/1年级下册（2025春）_Part1_P1-33.pdf', first_page=5, last_page=5)
images[0].save('primary-school-fun-learning/temp/page_5.jpg', 'JPEG')
print("✅ Page 5 saved as image.")
