# 息壤

<div align="center">

**知你进取，共此生息。**

**息壤，更懂你节奏的情感陪伴型自学引擎。**

一个 AI 驱动、带有情感陪伴的个性化自学引擎：把模糊的学习愿望，培育成可执行、可反馈、会自我调整的成长路径。

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

[简体中文](README.md) | [English](README.en.md)

</div>

---

## 🌱 为什么是息壤？

在中国神话《山海经》里，息壤是一种永不耗减的神土——它随水而长，愈用愈生。知识的积淀，恰如这方神土：只要你肯持续投注心力，它便会自行蔓延、生长，最终筑成你精神的城池。

**你是否也曾有过一个学习目标，清晰却沉重，搁置在心底迟迟不知从何落笔？**

**你是否也曾启动过一个学习计划，开头几日意气风发，而后却在日复一日中悄然中断？**

**你是否也曾在某个瓶颈前反复挣扎，最终被挫败感和自我怀疑吞没？**

息壤懂你的困顿，它将你的学习任务，化为与一株“中草药精灵”共同成长的旅程——知识如药，而学习，是一场自我的疗愈。

现代人的焦虑与迷茫，何尝不是一种时代的“症候”？而自学，正是你为自己开出的方子。

*你若勤勉，那株药草便灵气盎然，枝叶舒展，足以安抚你内心的焦躁；*

*你若懈怠，它便萎顿低垂，无声地提醒你——精神的慰藉，从不凭空而来。*

**愿息壤之上，你的每一分努力，都生根发芽，终成一片属于自己的良药之林。**

## 📸 产品体验

![息壤产品演示](docs/demo.gif)

## ✨ 核心特性

- 🔍 **AI 坐诊——四诊定制，开出你的第一张“药方”**  
  望，诊你当下的状态；闻，听你真正的目标；问，理清你可用的时间；切，生成一份专属学习方案。不凭感觉，不靠硬撑，AI为你把脉定方。

- 🌿 **可视化成长——养一株草药，看得见坚持的回响**  
  开盲盒般召唤你的中草药精灵，每一次学习，都化作它的生长——发芽、舒展、繁茂。进度不再是一个冰冷数字，而是一个在呼吸的生命。

- 💬 **情感陪伴——它不说话，却在你最想放弃时开口**  
  工作台内置精灵对话，你完成了，它为你欢喜；你卡住了，它给你鼓励；你中断了，它不责备，只轻声提醒：回来就好。

- 🧪 **阶段检验与调整——走在偏了的路上，停下来就是进步**  
  阶段性复盘你的反馈，未达标时自动修正后续路径。学错了方向，比不学更可怕——它会帮你及时调头。

- 🎯 **终极反馈与增强——终点不是结束，是新的起点**  
  目标达成，为你庆祝；目标未达，自动生成增强计划。不让你空手而归，也不让你带着遗憾结束。

## 🛠️ 技术栈与架构

| 层级 | 技术 |
| --- | --- |
| 前端 | Next.js、React、Tailwind CSS、Framer Motion、Lucide React、Zustand |
| 后端 | Python、Flask、SQLAlchemy、Celery |
| 数据与任务 | PostgreSQL、Redis |
| AI 与工作流 | Ollama、LangChain、LangGraph |
| 搜索与部署 | SearXNG、Docker Compose |

```text
xira/
├── backend/          # Flask API、业务服务、数据模型与AI工作流
├── dev/              # 本地开发初始化与启动脚本
├── docker/           # PostgreSQL、Redis、Ollama、SearXNG
├── frontend/         # Next.js应用
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.12
- Node.js 与 npm
- Docker（启动 PostgreSQL、Redis、Ollama、SearXNG）

### 一键初始化

在项目根目录执行：

```bash
conda create -n xira-dev python=3.12 -y
conda activate xira-dev
./dev/setup
```

该脚本会创建 `backend/.venv`、安装 Python 与前端依赖，并生成 `backend/.env` 与 `frontend/.env.local`。

### 配置

初始化后按需修改：

- [backend/.env](backend/.env)：Flask、JWT、数据库、Redis、Celery、Ollama、SearXNG。
    - 生成 `SECRET_KEY` 

  bash for Linux

  ```bash
  cd backend
  sed -i "/^SECRET_KEY=/c\\SECRET_KEY=$(openssl rand -base64 42)" .env
  ```

  bash for Mac

  ```bash
  cd backend
  secret_key=$(openssl rand -base64 42)
  sed -i '' "/^SECRET_KEY=/c\\
  SECRET_KEY=${secret_key}" .env
  ```
- [frontend/.env.local](frontend/.env.local)：前端通过 `NEXT_PUBLIC_API_BASE` 指向后端 API。
  
开发环境默认服务端口：前端 `3000`、API `5000`、SearXNG `8080`、PostgreSQL `5432`、Redis `6379`、Ollama `11434`。

### 启动服务

分别打开终端窗口在项目根目录执行：

```bash
# 终端 1：启动基础设施，并拉取 qwen2.5:7b
./dev/start-docker-compose

# 终端 2：启动 Flask API（http://127.0.0.1:5000）
./dev/start-backend

# 终端 3：启动 Celery worker
./dev/start-worker

# 终端 4：启动 Next.js（http://localhost:3000）
./dev/start-frontend
```

浏览器访问 [http://localhost:3000](http://localhost:3000)。后端健康检查为 `GET http://127.0.0.1:5000/api/health`。

## 🗺️ Roadmap

- [x] 四诊定制学习计划
- [x] 学习打卡、精灵成长与中断状态
- [x] 阶段检验、学习计划调整与结果反馈闭环
- [ ] 中草药精灵表情包/动画
- [ ] 开盲盒生成中草药精灵的时候，会考虑稀有度权重，越稀有的中草药越难开出来
- [ ] 社区版可以分享自己的学习计划，他人可以直接执行优秀的学习计划

## 🤝 贡献与反馈

欢迎通过 Issue 反馈问题、提出想法，或提交 Pull Request。提交代码前，请先确认后端测试与前端构建可以通过：

```bash
cd backend && pytest
cd frontend && npm run build
```

## 🙏 致谢

- [SearXNG](https://github.com/searxng/searxng)：隐私友好的元搜索引擎。
- [Ollama](https://ollama.com/)：本地大语言模型运行环境。
- [LangChain](https://www.langchain.com/) 与 [LangGraph](https://www.langchain.com/langgraph)：LLM 应用与工作流编排。

## 📄 许可

本项目采用 [Apache License 2.0](LICENSE) 开源。