# 📖 操作手册 (User Manual)

本手册将指导您如何使用自动化脚本来添加新课文。

## 场景 A: 我有 Google Gemini API Key
这是最理想的全自动模式。

1.  复制 `.env.example` 为 `.env`。
2.  在 `.env` 中填入 `GEMINI_API_KEY`。
3.  将 PDF 文件（如 `lesson.pdf`）放入项目根目录。
4.  运行命令：
    ```bash
    python3 scripts/auto_deploy.py "lesson.pdf"
    ```
5.  喝杯咖啡 ☕️，脚本会自动完成解析、配图和发布。

---

## 场景 B: 我没有 API Key (当前环境)
您依然可以半自动地完成工作。

### 步骤 1: 准备内容 (JSON)
由于无法调用 Gemini，您需要手动（或请 AI 助手）将课文内容整理为 JSON 格式，保存到 `temp/parsed_lesson.json`。

**JSON 格式示例**:
```json
[
  {
    "subject": "Chinese",
    "title": "新课文标题",
    "content": {
      "subject": "语文",
      "title": "新课文标题",
      "category": "识字",
      "vocabulary": [
        {"word": "苹果", "definition": "Apple"},
        {"word": "香蕉", "definition": "Banana"}
      ],
      "sentences": ["我爱吃水果。"]
    }
  }
]
```

### 步骤 2: 运行脚本
直接运行 `auto_deploy.py`，并指定任意 PDF 文件名（即使 PDF 没解析成功也不要紧）：

```bash
python3 scripts/auto_deploy.py "dummy.pdf"
```

### 步骤 3: 脚本自动接管
脚本会：
1.  尝试解析 PDF -> 失败。
2.  **自动检测到 `temp/parsed_lesson.json` 存在** -> 读取您的 JSON。
3.  **自动配图** -> 遍历 "Apple", "Banana"，从网络下载插图。
4.  **自动部署** -> 更新网页。

---

## ❓ 常见问题

### Q1: 配图失败怎么办？
脚本会自动跳过失败的图片，网页上会显示文字。您也可以手动找一张图放入 `assets/images/`，文件名为 `生字.jpg`（如 `苹果.jpg`），脚本下次运行时会自动识别并关联。

### Q2: 如何修改已发布的课文？
只需在 JSON 中修改内容，确保 `title` 不变。再次运行脚本时，它会检测到相同标题，自动执行**更新 (Update)** 而非新增。

### Q3: 数学课不显示图形？
请确保数学课的 JSON 中包含 `shapes` 数组。如果是算术课，请确保不包含 `shapes`，而是包含 `formulas` 或 `key_concepts`。
