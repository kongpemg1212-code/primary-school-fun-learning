# Primary School Fun Learning (小学趣味学习系统)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Vue 3](https://img.shields.io/badge/Vue-3.x-green)
![Status](https://img.shields.io/badge/status-active-success)

一个基于 AI 驱动的小学语文与数学趣味学习 Web 应用。旨在通过互动式体验帮助小学生巩固识字、背诵古诗、理解数学概念。

🔗 **在线演示**: [GitHub Pages Link](https://kongpemg1212-code.github.io/primary-school-fun-learning/)

---

## ✨ 核心功能 (Features)

### 📖 语文模块 (Chinese)
- **识字卡片**: 每一课生字自动配图（AI 生成/网络抓取），点击可朗读（需浏览器支持）。
- **古诗背诵**: 独创“渐进式挖空”背诵模式（Level 1-4），帮助孩子科学记忆。
- **语序挑战**: 拖拽拼句游戏，锻炼语感。

### 🔢 数学模块 (Math)
- **几何画板**: 交互式 Canvas 画布，拖动控制点改变图形（长方形、三角形、圆）。
- **公式与概念**: 清晰展示核心数学公式（如破十法）和知识点卡片。
- **互动练习**: 简单的数学问答交互。

### 🤖 自动化工作流 (AI Workflow)
- **一键解析**: 支持上传 PDF 教材（如《语文一年级下册》），自动提取课文内容。
- **智能配图**: 脚本自动识别生字，调用 Pollinations AI 或 Lorem Flickr 获取插图。
- **自动部署**: 运行脚本后，自动合并数据、生成图片、提交 Git 并触发 GitHub Pages 更新。

---

## 🚀 快速开始 (Quick Start)

### 1. 环境准备
确保已安装 Python 3.10+ 和 Git。

```bash
git clone https://github.com/kongpemg1212-code/primary-school-fun-learning.git
cd primary-school-fun-learning
pip install -r requirements.txt
```

### 2. 配置 (可选)
如果需要使用 Gemini 解析 PDF 或 DALL-E 配图，请配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 填入 GEMINI_API_KEY 或 OPENAI_API_KEY
# (如果没有 Key，脚本会自动降级使用免费图源或手动数据模式)
```

### 3. 添加新课文 (全自动模式)
将 PDF 文件放入项目目录，运行：
```bash
python3 scripts/auto_deploy.py "your_textbook.pdf"
```
脚本将自动完成：
1. 解析 PDF -> JSON
2. 下载配图 -> `assets/images/`
3. 更新数据库 -> `data/lessons.json`
4. 提交代码 -> `git push`

---

## 📂 项目结构

```
primary-school-fun-learning/
├── assets/             # 静态资源
│   └── images/         # 课文配图 (自动下载)
├── data/               # 数据存储
│   └── lessons.json    # 核心课程数据库
├── scripts/            # 自动化脚本
│   ├── auto_deploy.py  # 总控脚本 (Deployer)
│   ├── smart_parser.py # PDF 解析器 (基于 Gemini)
│   └── illustrator.py  # 配图生成器 (支持 Pollinations/Unsplash)
├── index.html          # 前端入口 (Vue 3 单页应用)
└── README.md           # 项目文档
```

## 🛠️ 技术栈
- **Frontend**: Vue 3 (CDN), TailwindCSS, Phosphor Icons, Rough.js (手绘风格库).
- **Backend (Scripts)**: Python 3, PyMuPDF, Requests.
- **AI Services**: Google Gemini 3.0 Pro (解析), Pollinations AI / Lorem Flickr (配图).

---

## 📝 维护指南
详见 [MANUAL.md](MANUAL.md) 操作手册。
技术架构请参考 [DESIGN.md](DESIGN.md)。
