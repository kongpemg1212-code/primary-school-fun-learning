import sqlite3

def init_edu_db(db_path="data/edu_system.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 1. 课程表 (Lessons)
    c.execute('''CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,      -- 'Chinese' or 'Math'
        title TEXT,
        content_json TEXT, -- 存储解析后的完整原始 JSON
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 2. 语文生词表 (Chinese Vocabulary)
    c.execute('''CREATE TABLE IF NOT EXISTS chinese_vocab (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        word TEXT,
        pronunciation TEXT,
        definition TEXT,
        example TEXT,
        image_url TEXT,
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    )''')
    
    # 3. 数学几何表 (Math Geometry)
    c.execute('''CREATE TABLE IF NOT EXISTS math_geometry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        shape_type TEXT,   -- 'rectangle', 'triangle', etc.
        params_json TEXT,  -- 存储图形坐标或宽高数据
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    )''')
    
    conn.commit()
    conn.close()
    print(f"✅ 教育系统数据库已初始化: {db_path}")

if __name__ == "__main__":
    init_edu_db()
