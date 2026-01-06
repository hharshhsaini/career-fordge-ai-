# 🧭 Career Forge - AI Career Navigator

AI-powered career guidance platform that helps students discover their ideal career path with personalized learning roadmaps.

Deployed Link - https://careerfordge.netlify.app/

## ✨ Features

- **AI-Powered Career Analysis** - GPT-4.1-nano analyzes your skills and interests to recommend the best career path
- **6-Step Learning Roadmap** - Structured beginner to advanced learning journey
- **Curated Resources** - Official documentation links, top Udemy/Coursera courses
- **YouTube Tutorials** - Auto-fetched full course videos (no shorts!)
- **Knowledge Quizzes** - 15 technical questions per step, 80% pass rate required
- **Progress Tracking** - Mark completed steps, visualize your journey
- **PDF Download** - Export your personalized roadmap

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Lucide Icons
- jsPDF for PDF generation

**Backend:**
- FastAPI (Python)
- Azure OpenAI (GPT-4.1-nano)
- YouTube scraping (no API needed)

**Deployment:**
- Frontend: Netlify / Azure Static Web Apps
- Backend: Render / Azure App Service

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with:
# QUIZ_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
# QUIZ_API_KEY=your_api_key
# QUIZ_DEPLOYMENT=gpt-4.1-nano
# QUIZ_API_VERSION=2024-05-01-preview

uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## 📁 Project Structure

```
career-forge/
├── backend/
│   ├── main.py              # FastAPI endpoints
│   ├── ai_service.py        # Career roadmap generation
│   ├── services/
│   │   ├── quiz_service.py  # Quiz generation
│   │   └── youtube_service.py # YouTube scraping
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main app
│   │   └── components/
│   │       ├── RoadmapCard.jsx
│   │       ├── QuizModal.jsx
│   │       ├── ProgressChart.jsx
│   │       └── LoadingAnimation.jsx
│   └── public/
│       └── favicon.png
└── README.md
```

## 🔑 Environment Variables

### Backend (Render)
| Variable | Description |
|----------|-------------|
| `QUIZ_ENDPOINT` | Azure Cognitive Services endpoint |
| `QUIZ_API_KEY` | Azure API key |
| `QUIZ_DEPLOYMENT` | Model deployment name (gpt-4.1-nano) |
| `QUIZ_API_VERSION` | API version (2024-05-01-preview) |

## 🎯 How It Works

1. **User Input** - Describe your background and interests
2. **AI Analysis** - GPT-4.1-nano generates personalized career recommendation
3. **Roadmap Generation** - 6-step learning path with resources
4. **YouTube Fetch** - Scrapes relevant full course tutorials
5. **Quiz Verification** - Pass 80% to mark step complete
6. **Progress Tracking** - Saved locally, visualize completion

## 📸 Screenshots

- 3D Loading Animation while generating
- Beautiful gradient UI with purple theme
- Interactive quiz modal with explanations
- Progress chart visualization

## 👨‍💻 Author

**Harsh Saini**

Made with ❤️ for Microsoft Azure Hackathon 2026

## 📄 License

MIT License
