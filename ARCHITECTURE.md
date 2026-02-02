# 🚀 CareerForge AI - Production Architecture

> **Mission**: 100% Open-Source, Zero API Costs, Infinite Scalability

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CAREERFORGE AI ARCHITECTURE                             │
│                          (100% Open-Source, Zero API Costs)                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐     ┌──────────────────────────────┐     ┌────────────────────┐
│                     │     │                              │     │                    │
│   FRONTEND          │     │   BACKEND API                │     │   LLM SERVICE      │
│   (React/Vite)      │     │   (FastAPI/Python)           │     │   (Ollama)         │
│                     │     │                              │     │                    │
│  ┌───────────────┐  │     │  ┌────────────────────────┐  │     │  ┌──────────────┐  │
│  │ Landing Page  │  │     │  │ POST /api/ai/roadmap   │  │     │  │              │  │
│  │ Career Form   │  │────▶│  │ POST /api/ai/skills    │──┼────▶│  │  Mistral 7B  │  │
│  │ Dashboard     │  │     │  │ POST /api/ai/interview │  │     │  │  Instruct    │  │
│  │ Progress      │  │◀────│  │ POST /api/ai/quiz      │◀─┼─────│  │  (Apache 2.0)│  │
│  └───────────────┘  │     │  └────────────────────────┘  │     │  └──────────────┘  │
│                     │     │                              │     │                    │
│  Port: 5173         │     │  ┌────────────────────────┐  │     │  REST API: 11434   │
│                     │     │  │ Prompt Engineering     │  │     │  OpenAI-compat.    │
│                     │     │  │ Response Validation    │  │     │                    │
│                     │     │  │ JSON Structuring       │  │     │  Hot-swappable:    │
│                     │     │  └────────────────────────┘  │     │  - Mistral 7B ✓    │
│                     │     │                              │     │  - LLaMA 3 8B      │
│                     │     │  Port: 8000                  │     │  - Mixtral 8x7B    │
│                     │     │                              │     │  - Qwen 7B         │
└─────────────────────┘     └──────────────────────────────┘     └────────────────────┘
```

---

## 🏆 Model Selection: Mistral 7B Instruct v0.3

### Why Mistral 7B?

| Criteria | Mistral 7B | LLaMA 3 8B | Mixtral 8x7B |
|----------|------------|------------|--------------|
| **License** | ✅ Apache 2.0 | ⚠️ Meta License | ✅ Apache 2.0 |
| **Commercial Use** | ✅ Unrestricted | ⚠️ Restrictions | ✅ Unrestricted |
| **VRAM (Q4)** | 6GB | 8GB | 24GB+ |
| **Speed** | ⚡ 127 tok/s | 67 tok/s | 45 tok/s |
| **Context** | 32K | 8K | 32K |
| **Reasoning** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### Key Advantages:
1. **True Apache 2.0** - Zero licensing friction for commercial use
2. **6GB VRAM** - Runs on RTX 3060/4060 consumer GPUs
3. **32K Context** - Handle detailed profiles and long roadmaps
4. **Fastest in class** - 2x faster than LLaMA 3 8B
5. **Battle-tested** - Production-proven with extensive community

---

## 📁 Project Structure

```
career-forge/
├── backend/
│   ├── main.py                     # FastAPI application entry
│   ├── config.py                   # Environment configuration
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── ai_routes.py        # AI endpoint handlers
│   │   │   ├── health_routes.py    # Health checks
│   │   │   └── quiz_routes.py      # Quiz endpoints
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── requests.py         # Request models
│   │       └── responses.py        # Response models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py          # LLM abstraction layer
│   │   ├── roadmap_service.py      # Roadmap generation
│   │   ├── skills_service.py       # Skills analysis
│   │   ├── interview_service.py    # Interview prep
│   │   ├── quiz_service.py         # Quiz generation
│   │   └── youtube_service.py      # YouTube scraping
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── system_prompts.py       # System prompts
│   │   ├── roadmap_prompts.py      # Roadmap templates
│   │   └── quiz_prompts.py         # Quiz templates
│   │
│   └── utils/
│       ├── __init__.py
│       ├── json_parser.py          # Safe JSON extraction
│       └── validators.py           # Input validation
│
├── llm-service/
│   ├── docker-compose.yml          # Ollama deployment
│   ├── Modelfile                   # Custom model config
│   └── scripts/
│       ├── setup.sh                # Setup script
│       ├── health-check.sh         # Health monitoring
│       └── benchmark.sh            # Performance testing
│
├── frontend/
│   └── [existing React/Vite app]
│
├── docker-compose.yml              # Full stack deployment
├── .env.example                    # Environment template
├── ARCHITECTURE.md                 # This file
└── README.md                       # Quick start guide
```

---

## 🔌 API Design

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/roadmap` | Generate career roadmap |
| `POST` | `/api/ai/skills` | Analyze and suggest skills |
| `POST` | `/api/ai/interview-prep` | Interview preparation |
| `POST` | `/api/ai/quiz` | Generate knowledge quiz |
| `GET` | `/api/health` | Service health check |
| `GET` | `/api/health/llm` | LLM service status |

### Response Format (Roadmap)

```json
{
  "success": true,
  "data": {
    "career_role": "Full-Stack Developer",
    "overview": "...",
    "timeline": "6-9 months",
    "roadmap": [
      {
        "month": 1,
        "title": "Foundation",
        "weeks": [
          {
            "week": 1,
            "focus": "HTML & CSS Fundamentals",
            "hours": 15,
            "tasks": ["Build personal portfolio", "Complete CSS Grid course"]
          }
        ],
        "tools": ["VS Code", "Git", "Chrome DevTools"],
        "projects": [
          {
            "name": "Personal Portfolio",
            "difficulty": "beginner",
            "estimated_hours": 10
          }
        ],
        "checkpoint": "Can build responsive layouts from scratch"
      }
    ],
    "final_outcome": "...",
    "resources": {
      "official_docs": [],
      "courses": [],
      "youtube_channels": []
    }
  },
  "meta": {
    "model": "mistral:7b-instruct-v0.3",
    "latency_ms": 2450,
    "tokens_used": 1847
  }
}
```

---

## 🚀 Deployment Options

### 1. Local Development (FREE)

```bash
# Terminal 1: Start LLM Service (Ollama)
ollama serve
ollama pull mistral:7b-instruct-v0.3-q4_K_M

# Terminal 2: Start Backend
cd backend && uvicorn main:app --reload

# Terminal 3: Start Frontend
cd frontend && npm run dev
```

**Requirements**: 8GB+ RAM, 10GB disk for model

### 2. Single VPS ($20-50/month)

- **Provider**: Hetzner, Contabo, or DigitalOcean
- **Specs**: 8 vCPU, 16GB RAM, 100GB SSD
- **Setup**: Docker Compose + Nginx reverse proxy

```bash
docker-compose up -d
```

### 3. Cheap GPU Server ($0.20-0.50/hour)

- **Provider**: RunPod, Vast.ai, or Lambda Labs
- **GPU**: RTX 3060 (12GB) or RTX 4060 Ti (16GB)
- **Performance**: <1s latency for most queries

### 4. Production (Scalable)

- **Kubernetes** with HPA for API pods
- **Ollama deployed as StatefulSet** with GPU node pool
- **Redis** for response caching
- **CDN** for frontend static assets

---

## 🔒 Security Considerations

1. **Rate Limiting**: 10 req/min per IP for AI endpoints
2. **Input Validation**: Strict schemas with Pydantic
3. **No Secrets in Code**: All config via environment variables
4. **CORS**: Restricted to known origins in production
5. **Prompt Injection Protection**: Input sanitization

---

## 📈 Future Enhancements

1. **Fine-tuning**: Train on career guidance datasets
2. **Model Upgrades**: Hot-swap to Mixtral when GPU available
3. **Caching Layer**: Redis for common roadmap patterns
4. **User Feedback Loop**: Improve prompts based on ratings
5. **Multi-modal**: Resume parsing with vision models

---

## 📄 License

This project is **MIT Licensed**. 
The LLM (Mistral 7B) is **Apache 2.0 Licensed**.
