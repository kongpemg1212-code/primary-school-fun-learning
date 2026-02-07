import sqlite3
import json
import os
import requests

DB_PATH = 'data/edu_system.db'
IMAGE_DIR = 'assets/images'

def download_image(url, filename):
    local_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(local_path):
        return local_path
    
    try:
        print(f"Downloading {url} to {local_path}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return url # Fallback to original URL if download fails

def seed_data():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 清空旧数据
    c.execute("DELETE FROM chinese_vocab")
    c.execute("DELETE FROM math_geometry")
    c.execute("DELETE FROM lessons")
    c.execute("DELETE FROM sqlite_sequence WHERE name IN ('lessons', 'chinese_vocab', 'math_geometry')")

    # 1. 语文课文：春夏秋冬
    chinese_content = {
        "subject": "语文",
        "title": "春夏秋冬",
        "category": "识字",
        "vocabulary": [
            {
                "word": "春风", 
                "pinyin": "chūn fēng", 
                "definition": "春天的风", 
                "example": "春风吹",
                "image_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=600",
                "local_name": "spring_breeze.jpg"
            },
            {
                "word": "夏雨", 
                "pinyin": "xià yǔ", 
                "definition": "夏天的雨", 
                "example": "夏雨落",
                "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600",
                "local_name": "summer_rain.jpg"
            },
            {
                "word": "秋霜", 
                "pinyin": "qiū shuāng", 
                "definition": "秋天的霜", 
                "example": "秋霜降",
                "image_url": "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=600",
                "local_name": "autumn_frost.jpg"
            },
            {
                "word": "冬雪", 
                "pinyin": "dōng xuě", 
                "definition": "冬天的雪", 
                "example": "冬雪飘",
                "image_url": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=600",
                "local_name": "winter_snow.jpg"
            }
        ],
        "sentences": ["春风吹", "夏雨落", "秋霜降", "冬雪飘"]
    }
    
    # Process images: Download and replace URLs with local paths
    processed_vocab = []
    for v in chinese_content['vocabulary']:
        local_path = download_image(v['image_url'], v['local_name'])
        # Store as relative path for web
        v['image'] = local_path 
        processed_vocab.append(v)
    
    chinese_content['vocabulary'] = processed_vocab

    c.execute("INSERT INTO lessons (subject, title, content_json) VALUES (?, ?, ?)",
              ("Chinese", "春夏秋冬", json.dumps(chinese_content, ensure_ascii=False)))
    lesson_id_zh = c.lastrowid
    
    for v in chinese_content['vocabulary']:
        c.execute("INSERT INTO chinese_vocab (lesson_id, word, pronunciation, definition, example, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                  (lesson_id_zh, v['word'], v['pinyin'], v['definition'], v['example'], v['image']))
    
    # 2. 数学课文：认识平面图形
    math_content = {
        "subject": "数学",
        "title": "认识平面图形",
        "shapes": [
            {"type": "rectangle", "name": "长方形", "desc": "四条边，四个直角，对边相等"},
            {"type": "square", "name": "正方形", "desc": "四条边都相等，四个直角"},
            {"type": "triangle", "name": "三角形", "desc": "三条边，三个角"},
            {"type": "circle", "name": "圆", "desc": "曲线围成的封闭图形"}
        ]
    }
    
    c.execute("INSERT INTO lessons (subject, title, content_json) VALUES (?, ?, ?)",
              ("Math", "认识平面图形", json.dumps(math_content, ensure_ascii=False)))
    lesson_id_ma = c.lastrowid
    
    for s in math_content['shapes']:
        c.execute("INSERT INTO math_geometry (lesson_id, shape_type, params_json) VALUES (?, ?, ?)",
                  (lesson_id_ma, s['type'], json.dumps(s, ensure_ascii=False)))
    
    conn.commit()
    
    # Export for Frontend
    c.execute("SELECT * FROM lessons")
    rows = c.fetchall()
    export_data = []
    for row in rows:
        export_data.append({
            "id": row[0],
            "subject": row[1],
            "title": row[2],
            "content": json.loads(row[3])
        })
    
    with open("data/lessons.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
        
    conn.close()
    print("✅ Local image sync complete. Database re-seeded.")

if __name__ == "__main__":
    seed_data()
