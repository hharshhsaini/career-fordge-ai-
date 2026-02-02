# 🚀 CareerForge AI - Open Source Career Guidance Platform

> **100% Open-Source • Zero API Costs • Self-Hosted LLM**

AI-powered career guidance platform that generates personalized learning roadmaps, skills analysis, and interview preparation — all running on your own infrastructure with **zero usage costs**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LLM: Mistral 7B](https://img.shields.io/badge/LLM-Mistral%207B-blue)](https://mistral.ai/)
[![License: Apache 2.0](https://img.shields.io/badge/Model%20License-Apache%202.0-green)](https://www.apache.org/licenses/LICENSE-2.0)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Career Roadmaps** | 6-month personalized learning paths with weekly breakdowns |
| 📚 **Skills Analysis** | Identify transferable skills and learning priorities |
| 💼 **Interview Prep** | Technical & behavioral questions with answer frameworks |
| 🧠 **Knowledge Quizzes** | 15 MCQs per step with explanations (80% pass rate) |
| 🎬 **YouTube Tutorials** | Auto-curated full course videos (no shorts!) |
| 📊 **Progress Tracking** | Visual completion tracking with PDF export |

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │     │   Backend API    │     │   LLM Service   │
│   (React/Vite)  │────▶│   (FastAPI)      │────▶│   (Ollama)      │
│   Port: 5173    │     │   Port: 8000     │     │   Port: 11434   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
                                                 ┌─────────────────┐
                                                 │  Mistral 7B     │
                                                 │  (Apache 2.0)   │
                                                 └─────────────────┘
```

## 🏆 Why Mistral 7B?

| Model | License | VRAM | Speed | Context |
|-------|---------|------|-------|---------|
| **Mistral 7B** ✓ | Apache 2.0 | 6GB | 127 tok/s | 32K |
| LLaMA 3 8B | Meta License* | 8GB | 67 tok/s | 8K |
| Mixtral 8x7B | Apache 2.0 | 24GB+ | 45 tok/s | 32K |

*Mistral 7B is truly open with zero licensing friction for commercial use.*

---

## 🚀 Quick Start

### Prerequisites

- **macOS/Linux** or WSL on Windows
- **8GB+ RAM** (16GB recommended)
- **Python 3.10+**
- **Node.js 18+**

### 1. Install Ollama & Model

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Download Mistral 7B (4.1GB, takes 2-5 minutes)
ollama pull mistral:7b-instruct-v0.3-q4_K_M
```

### 2. Start Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
uvicorn main_v2:app --reload --port 8000
```

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the App

Visit **http://localhost:5173** 🎉

---

## 📡 API Endpoints

### Core AI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/roadmap` | Generate career roadmap |
| `POST` | `/api/ai/skills` | Analyze skills & recommendations |
| `POST` | `/api/ai/interview-prep` | Interview preparation guide |
| `POST` | `/api/ai/quiz` | Generate knowledge quiz |

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | System health status |
| `GET` | `/api/health/llm` | LLM service status |
| `GET` | `/api/health/models` | Available models |

### Legacy Compatibility

| Method | Endpoint | Maps To |
|--------|----------|---------|
| `POST` | `/generate-path` | `/api/ai/roadmap` |
| `POST` | `/generate-quiz` | `/api/ai/quiz` |

**Full API docs**: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### Quick Start (All Services)

```bash
# Clone and run everything
docker-compose up -d

# Wait for model to download (first run only)
docker-compose logs -f model-loader
```

### Individual Services

```bash
# Just the LLM service
cd llm-service
docker-compose up -d

# Verify it's running
curl http://localhost:11434/api/tags
```

---

## ☁️ Deployment Options

### 1. Local Machine (FREE)

- **Hardware**: 8GB RAM, any modern CPU
- **Performance**: ~3-5s per roadmap generation
- **Best for**: Development, personal use

### 2. Single VPS ($20-50/month)

```
Provider     RAM    vCPUs   Cost/mo
─────────────────────────────────────
Hetzner      16GB   4       $18
Contabo      16GB   4       $12
DigitalOcean 16GB   4       $48
```

### 3. GPU Cloud ($0.20-0.50/hour)

```
Provider   GPU          VRAM   Cost/hr
────────────────────────────────────────
RunPod     RTX 3060     12GB   $0.20
Vast.ai    RTX 3080     10GB   $0.25
Lambda     RTX 4090     24GB   $0.50
```

**GPU gives 10-20x faster inference!**

---

## 📁 Project Structure

```
career-forge/
├── backend/
│   ├── main_v2.py              # FastAPI app (open-source LLM)
│   ├── config.py               # Environment configuration
│   ├── api/
│   │   ├── routes/             # API endpoint handlers
│   │   └── schemas/            # Request/response models
│   ├── services/
│   │   ├── llm_service.py      # Ollama integration
│   │   ├── roadmap_service.py  # Roadmap generation
│   │   ├── skills_service.py   # Skills analysis
│   │   ├── interview_service.py # Interview prep
│   │   └── quiz_service_v2.py  # Quiz generation
│   ├── prompts/                # Prompt templates
│   └── utils/                  # Helpers
│
├── llm-service/
│   ├── docker-compose.yml      # Ollama deployment
│   ├── Modelfile               # Custom model config
│   └── scripts/
│       ├── setup.sh            # Installation script
│       ├── health-check.sh     # Monitoring
│       └── benchmark.sh        # Performance testing
│
├── frontend/                   # React/Vite app
├── docker-compose.yml          # Full stack deployment
└── ARCHITECTURE.md             # Detailed architecture docs
```

---

## 🔧 Configuration

All settings via environment variables:

```bash
# LLM Service
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=mistral:7b-instruct-v0.3-q4_K_M
LLM_TIMEOUT=120

# API Server
API_PORT=8000
CORS_ORIGINS=http://localhost:5173

# Features
YOUTUBE_ENABLED=true
RATE_LIMIT=30
```

See `.env.example` for all options.

---

## 🔒 Security

- ✅ Rate limiting on AI endpoints
- ✅ Input validation & sanitization
- ✅ Prompt injection protection
- ✅ No secrets in code
- ✅ CORS configuration
- ✅ Non-root Docker containers

---

## 🚀 Scaling Notes

### Horizontal Scaling

```yaml
# deploy.yaml (Kubernetes)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: careerforge-api
spec:
  replicas: 3  # Scale API pods
  ...
```

### Response Caching

Add Redis for caching common roadmaps:
```python
# Cache similar profile queries
cache_key = hash(user_profile)
if cached := redis.get(cache_key):
    return cached
```

### Model Upgrades

Hot-swap to stronger models when resources available:
```bash
# Upgrade to Mixtral (needs 24GB+ VRAM)
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M

# Update .env
LLM_MODEL=mixtral:8x7b-instruct-v0.1-q4_K_M
```

---

## 📸 Screenshots

*Beautiful gradient UI with purple theme, 3D loading animations, interactive quiz modals, and progress visualization.*

---

## 🛠️ Development

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Lint & Format

```bash
black .
isort .
mypy .
```

### Benchmark LLM

```bash
cd llm-service/scripts
./benchmark.sh
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

- **This Project**: MIT License
- **Mistral 7B Model**: Apache 2.0 License

---

## 👨‍💻 Author

**Harsh Saini**

Made with ❤️ for developers who want AI without the API bill.

---

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) for the amazing open-source model
- [Ollama](https://ollama.com/) for making local LLM deployment easy
- The open-source community for making this possible

---

*"BC… ye banda serious hai."* 🚀
