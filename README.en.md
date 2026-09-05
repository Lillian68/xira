# Xira

<div align="center">

**Your growth, nurtured. Never study alone.**

**Let Xira be the companion who truly understands your pace.**

An AI-powered personalized self-learning engine with emotional support.

It turns vague learning goals into actionable, trackable growth paths that continuously adapt to you.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

[简体中文](README.md) | [English](README.en.md)

</div>

---

## 🌱 Why Xira?

In the Chinese classic *The Classic of Mountains and Seas*, Xirang is a miraculous soil that never runs out. It grows with water, becoming more abundant the more it is used. Learning is much the same: when you keep investing effort, knowledge takes root and gradually builds a world of your own.

**Have you ever had a learning goal that was clear but overwhelming, sitting in the back of your mind because you did not know where to begin?**

**Have you ever started a study plan with energy and determination, only to quietly abandon it after a few days?**

**Have you ever struggled at a difficult point until frustration and self-doubt took over?**

Xira understands these moments. It turns your learning tasks into a journey with a growing herbal spirit: knowledge becomes medicine, and learning becomes a way to care for yourself.

Your herbal spirit grows when you stay committed and gently reminds you to return when you fall behind. Every minute of effort can take root and become part of your own forest of knowledge.

## 📸 Product Demo

![Xira product demo](docs/demo.gif)

## ✨ Core Features

- 🔍 **AI diagnosis and personalized planning**  
  Four-step discovery of your current state, true goals, available time, and a practical learning plan.

- 🌿 **Visible growth**  
  Summon a herbal spirit and watch each study session become visible growth: sprouting, stretching, and flourishing.

- 💬 **Emotional companionship**  
  Your spirit celebrates progress, offers encouragement when you are stuck, and welcomes you back without blame when you pause.

- 🧪 **Milestone reviews and adaptation**  
  Periodic reviews use your feedback to adjust the path when the current direction is not working.

- 🎯 **Final feedback and reinforcement**  
  Celebrate completed goals or receive an enhanced plan so every journey ends with a useful next step.

## 🛠️ Technology Stack

| Layer | Technologies |
| --- | --- |
| Frontend | Next.js, React, Tailwind CSS, Framer Motion, Lucide React, Zustand |
| Backend | Python, Flask, SQLAlchemy, Celery |
| Data and jobs | PostgreSQL, Redis |
| AI and workflows | Ollama, LangChain, LangGraph |
| Search and deployment | SearXNG, Docker Compose |

```text
xira/
├── backend/          # Flask API, services, data models, and AI workflows
├── dev/              # Local setup and startup scripts
├── docker/           # PostgreSQL, Redis, Ollama, and SearXNG
├── frontend/         # Next.js application
└── README.md
```

## 🚀 Quick Start

### Requirements

- Python 3.12
- Node.js and npm
- Docker for PostgreSQL, Redis, Ollama, and SearXNG

### Initialize

From the project root:

```bash
conda create -n xira-dev python=3.12 -y
conda activate xira-dev
./dev/setup
```

The script creates `backend/.venv`, installs backend and frontend dependencies, and generates `backend/.env` and `frontend/.env.local`.

### Configuration

After initialization, update the generated configuration as needed:

- [backend/.env](backend/.env): Flask, JWT, database, Redis, Celery, Ollama, and SearXNG settings.
    - generate `SECRET_KEY` 

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
- [frontend/.env.local](frontend/.env.local): set `NEXT_PUBLIC_API_BASE` to the backend API URL.

Default development ports are: frontend `3000`, API `5000`, SearXNG `8080`, PostgreSQL `5432`, Redis `6379`, and Ollama `11434`.

### Start Services

Open separate terminal windows and run these commands from the project root:

```bash
# Terminal 1: start infrastructure and pull qwen2.5:7b
./dev/start-docker-compose

# Terminal 2: start the Flask API at http://127.0.0.1:5000
./dev/start-backend

# Terminal 3: start the Celery worker
./dev/start-worker

# Terminal 4: start Next.js at http://localhost:3000
./dev/start-frontend
```

Open [http://localhost:3000](http://localhost:3000) in your browser. The backend health check is `GET http://127.0.0.1:5000/api/health`.

## 🗺️ Roadmap

- [x] Four-step personalized learning plans
- [x] Study check-ins, spirit growth, and interruption states
- [x] Milestone reviews, plan adjustment, and feedback loops
- [ ] Herbal spirit sticker packs and animations
- [ ] Rarity-based weighting for herbal spirit discovery
- [ ] Community sharing and reuse of excellent learning plans

## 🤝 Contributing and Feedback

Issues, ideas, and pull requests are welcome. Before submitting code, make sure the backend tests and frontend build pass:

```bash
cd backend && pytest
cd frontend && npm run build
```

## 🙏 Acknowledgements

- [SearXNG](https://github.com/searxng/searxng): a privacy-respecting metasearch engine.
- [Ollama](https://ollama.com/): a local environment for running language models.
- [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langchain.com/langgraph): LLM application and workflow orchestration.

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
