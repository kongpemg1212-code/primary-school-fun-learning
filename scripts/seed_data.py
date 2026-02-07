import sqlite3
import json

DB_PATH = 'data/edu_system.db'

def seed_initial_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
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
                "image": "https://image.pollinations.ai/prompt/beautiful%20digital%20painting%20of%20gentle%20spring%20breeze%20blowing%20through%20pink%20cherry%20blossoms%20soft%20colors%20kids%20illustration?width=600&height=400&nologo=true"
            },
            {
                "word": "夏雨", 
                "pinyin": "xià yǔ", 
                "definition": "夏天的雨", 
                "example": "夏雨落",
                "image": "https://image.pollinations.ai/prompt/cute%20illustration%20of%20summer%20rain%20falling%20on%20green%20lotus%20leaves%20in%20a%20pond%20vibrant%20colors%20kids%20style?width=600&height=400&nologo=true"
            },
            {
                "word": "秋霜", 
                "pinyin": "qiū shuāng", 
                "definition": "秋天的霜", 
                "example": "秋霜降",
                "image": "https://image.pollinations.ai/prompt/artistic%20kids%20illustration%20of%20white%20frost%20on%20red%20maple%20leaves%20in%20autumn%20crisp%20morning%20light?width=600&height=400&nologo=true"
            },
            {
                "word": "冬雪", 
                "pinyin": "dōng xuě", 
                "definition": "冬天的雪", 
                "example": "冬雪飘",
                "image": "https://image.pollinations.ai/prompt/whimsical%20illustration%20of%20soft%20white%20snow%20falling%20on%20a%20small%20wooden%20house%20winter%20wonderland%20kids%20book%20style?width=600&height=400&nologo=true"
            }
        ],
        "sentences": ["春风吹", "夏雨落", "秋霜降", "冬雪飘"]
    }
    
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
    print("✅ Initial data seeded and exported to data/lessons.json")

if __name__ == "__main__":
    seed_initial_data()
