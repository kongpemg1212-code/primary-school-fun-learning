import os
import json
import base64
from pathlib import Path

# 注意：此脚本设计为在 OpenClaw 环境下通过 Agent 辅助运行
# 核心逻辑：利用 Gemini 的多模态能力直接从视觉信息中提取教育知识点

def generate_parsing_prompt(subject="语文"):
    if subject == "语文":
        return """
        你是一个小学语文教育专家。请分析这张图片（或PDF页面），提取其中的核心学习内容。
        输出格式必须为严格的 JSON，包含以下字段：
        {
          "subject": "语文",
          "title": "课文标题",
          "vocabulary": [
            {"word": "生词", "pronunciation": "音标", "definition": "解释", "example": "简单例句"}
          ],
          "poem": {
            "title": "古诗标题",
            "author": "作者",
            "lines": ["第一句", "第二句", "..."]
          },
          "key_sentences": ["核心优美句子1", "核心优美句子2"]
        }
        """
    elif subject == "数学":
        return """
        你是一个小学数学教育专家。请分析这张图片，提取其中的几何图形或数学题。
        输出格式必须为严格的 JSON，包含以下字段：
        {
          "subject": "数学",
          "shapes": [
            {"type": "rectangle/triangle/circle", "properties": {"width": 10, "height": 5, "base": 8}, "description": "题目描述"}
          ],
          "problems": ["题目文本1", "题目文本2"]
        }
        """

# 模拟解析动作（在实际运行中，由 Agent 调用底层 API 完成）
def save_parsed_data(data, filename="parsed_lesson.json"):
    output_path = Path("data") / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ 数据已解析并保存至: {output_path}")

if __name__ == "__main__":
    print("🚀 Gemini Vision Parser Ready.")
    # 示例结构
    demo_data = {
        "subject": "语文",
        "title": "静夜思",
        "poem": {
            "title": "静夜思",
            "author": "李白",
            "lines": ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"]
        }
    }
    save_parsed_data(demo_data)
