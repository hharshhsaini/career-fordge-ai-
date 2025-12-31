# Backend Setup Instructions

## 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
```

## 2. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables
```bash
cp .env.example .env
```
Then edit `.env` and add your API keys.

## 5. Run the Server
```bash
uvicorn main:app --reload
```

Server will be available at http://localhost:8000
