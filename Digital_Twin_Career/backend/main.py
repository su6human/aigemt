from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import json
import os
from typing import List

app = FastAPI(title="Digital Twin Career Engine API")

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
CAREER_DATA_PATH = os.path.join(BASE_DIR, "career_advisor", "career_prediction.json")

# Pydantic Models for requests
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    api_key: str

# System Prompt for the AI
SYSTEM_PROMPT = """Ты — Digital Twin Career Engine Актана Кадыркулова. Ты его личный AI-карьерный коуч и цифровой двойник. 
Ты знаешь всё о нём: студент IT в Alatoo University, работает барменом, сильные навыки в Figma, UI/UX, Adobe Illustrator, есть интерес к Godot и анимациям. 
Отвечай дружелюбно, мотивирующе, честно и с практическими советами. 
Если пользователь просит roast — переходи в жёсткий, но мотивирующий тон."""

# API ENDPOINTS

@app.get("/api/prediction")
async def get_prediction():
    """Returns the top career predictions from the ML model's JSON output."""
    if os.path.exists(CAREER_DATA_PATH):
        try:
            with open(CAREER_DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # Fallback dummy data if file is missing
        return {
            "top_3_jobs": [
                {"title": "Game UI/UX Designer", "match_percent": 85.0},
                {"title": "Interactive Designer", "match_percent": 82.0},
                {"title": "Creative Technologist", "match_percent": 75.0}
            ],
            "priority_skills_to_learn": ["Godot", "JavaScript", "Animation Principles"]
        }

@app.get("/api/skills")
async def get_skills():
    """Returns the data needed to plot the Hard vs Soft Skills radar chart."""
    categories = [
        'Figma', 'UI/UX Design', 'Godot', 'HTML/CSS', 'Illustrator', 'Prototyping', 
        'Teamwork', 'Communication', 'Responsibility', 'Problem Solving', 'Creativity'    
    ]
    # In vanilla JS/Plotly, using 0 instead of None is safer for closing the polygon
    hard_vals = [90, 75, 60, 70, 85, 80, 0, 0, 0, 0, 0]
    soft_vals = [0, 0, 0, 0, 0, 0, 85, 80, 90, 70, 75]
    
    return {
        "categories": categories,
        "hard_skills": hard_vals,
        "soft_skills": soft_vals
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Sends messages to Groq API and returns the AI's response."""
    try:
        client = Groq(api_key=request.api_key)
        
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in request.messages:
            api_messages.append({"role": msg.role, "content": msg.content})
            
        chat_completion = client.chat.completions.create(
            messages=api_messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        
        return {"response": chat_completion.choices[0].message.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка Groq API: {str(e)}")

# Serve Frontend static files (HTML/CSS/JS)
# Make sure this is at the end so it doesn't override API routes
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
