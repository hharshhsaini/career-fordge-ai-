# 🔥 Career Forge - AI Career Navigator

An intelligent career guidance platform that helps students discover their ideal career path with personalized learning roadmaps and curated resources.

**Built for Microsoft Imagine Cup 2026**

🌐 **Live Demo:** [https://careerfordge.netlify.app](https://careerfordge.netlify.app)

## 🎯 What it Does

Career Forge analyzes your skills, education, and interests using AI to:

- Recommend the best-fit career role with detailed explanation
- Generate a comprehensive 6-step learning roadmap (Beginner → Advanced)
- Provide curated, high-quality resources for each step:
  - ✅ Official documentation links (verified URLs)
  - ✅ Top-rated paid courses (Udemy/Coursera recommendations)
  - ✅ Free YouTube video lectures (filtered for long-form content only)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python (FastAPI) |
| Frontend | React (Vite) + Tailwind CSS |
| AI | Google Gemini API |
| Data | YouTube Data API v3 |

## ✨ Key Features

- **Quality over Quantity** - Only verified, high-rated resources
- **Long-form Video Filtering** - Videos >20 minutes to ensure full courses, not clips
- **Complete Syllabus Coverage** - From fundamentals to interview preparation
- **Official Docs Priority** - Direct links to official documentation
- **Smart Fallbacks** - Works even when APIs hit rate limits

## 📁 Project Structure

```
career-forge/
├── backend/
│   ├── main.py              # FastAPI endpoints
│   ├── ai_service.py        # Gemini AI integration
│   ├── youtube_service.py   # YouTube API with quality filters
│   ├── requirements.txt
│   └── .env
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           └── RoadmapCard.jsx
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Gemini API Key
- YouTube Data API Key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/career-forge.git
cd career-forge
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```
### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/generate-path` | Generate career roadmap with curated resources |

### Sample Request

```bash
curl -X POST http://localhost:8000/generate-path \
  -H "Content-Type: application/json" \
  -d '{"description": "I am a BCA student knowing Python and interested in data science"}'
```

## 🧪 Demo Script

Copy-paste this into the app to test:

```
I am a 3rd year BCA student. I know Python basics, have done some web development with HTML/CSS, and recently started learning about databases. I'm really interested in data and how companies use it to make decisions.
```

## 📸 Screenshots

*Coming soon*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

---

**Made with ❤️ for Microsoft Imagine Cup 2026**
