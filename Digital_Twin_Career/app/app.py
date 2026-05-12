import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from groq import Groq

# --- Page Config ---
st.set_page_config(
    page_title="Digital Twin Career Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS (Dark Theme, Green/Purple Accents, Chat Styles) ---
st.markdown("""
<style>
    .main {
        background-color: #0d0f14;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        color: #00ffcc !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
    .subtitle {
        color: #a0a0a0;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .greeting {
        font-size: 1.1rem;
        color: #e0e0e0;
        background: #151821;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #b366ff;
        margin-bottom: 2rem;
    }
    .job-card {
        background: linear-gradient(135deg, rgba(0,255,204,0.1) 0%, rgba(179,102,255,0.1) 100%);
        border: 1px solid #b366ff;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(179,102,255,0.2);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc 0%, #b366ff 100%);
        color: #0d0f14;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.4);
        color: #ffffff;
    }
    .roast-box {
        background-color: #2a1118;
        border: 2px solid #ff0055;
        padding: 20px;
        border-radius: 12px;
        color: #ffcccc;
        font-size: 1.2rem;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.3);
    }
    
    /* Live Coach Chat Styles */
    div[data-testid="stChatMessage"] {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 15px;
        display: flex;
    }
    
    /* User Message (Right aligned, Blue) */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]), 
    div[data-testid="stChatMessage"]:has(svg[aria-label="user"]) {
        background-color: rgba(0, 123, 255, 0.1);
        border-right: 4px solid #007bff;
        border-radius: 20px 0 20px 20px;
        flex-direction: row-reverse;
        text-align: right;
    }
    
    /* Assistant Message (Left aligned, Purple/Green) */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
    div[data-testid="stChatMessage"]:has(svg[aria-label="assistant"]) {
        background-color: rgba(179, 102, 255, 0.1);
        border-left: 4px solid #b366ff;
        border-radius: 0 20px 20px 20px;
    }
    
    /* Fix text margin when reversed */
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
        margin-right: 15px;
        margin-left: 0;
    }
    div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
        margin-left: 15px;
        margin-right: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Load JSON Data ---
@st.cache_data
def load_data():
    json_path = r"C:\Users\aktan\.gemini\antigravity\scratch\career_advisor\career_prediction.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

data = load_data()

# --- Sidebar ---
st.sidebar.markdown("### 🧑‍💻 Актан Кадыркулов")
st.sidebar.markdown("🎓 **Статус:** Студент IT + Бармен")
st.sidebar.markdown("⚙️ *Digital Twin v0.4*")
st.sidebar.divider()

# Groq API Key Input
st.sidebar.markdown("### 🔑 Настройки AI")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Введи свой ключ Groq для общения с AI-коучем.")
if groq_api_key:
    st.session_state.groq_api_key = groq_api_key

st.sidebar.divider()

page = st.sidebar.radio("Навигация:", [
    "🏠 Home", 
    "📈 Career Prediction", 
    "⚖️ Balance Wheel", 
    "🌳 RPG Tech Tree", 
    "💬 Live Coach", 
    "🔥 Roast My Stack"
])

# --- Pages Routing ---

if page == "🏠 Home":
    st.markdown("<h1>Мой Digital Twin Career Engine</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>📍 Актан Кадыркулов • Бишкек</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='greeting'>🤖 <b>Я твой личный AI-карьерный двойник. Давай расти вместе!</b></div>", unsafe_allow_html=True)
    
    st.subheader("🎯 Твоя главная карьерная цель")
    
    top_title = "Game UI/UX Designer / Interactive Designer"
    top_match = 85.0
    
    if data and "recommended_path" in data:
        top_title = data["recommended_path"]
    elif data and "top_3_jobs" in data and len(data["top_3_jobs"]) > 0:
        top_title = data["top_3_jobs"][0]['title']
        top_match = data["top_3_jobs"][0]['match_percent']

    st.markdown(f"""
    <div class="job-card">
        <h2 style="color: #00ffcc; margin-top: 0;">🎮 {top_title}</h2>
        <p style="font-size: 1.1rem; color: #d0d0d0;">Идеальное сочетание твоих навыков дизайна и интереса к интерактивам/играм.</p>
        <p style="color: #b366ff; font-weight: bold; margin-bottom: 0;">⚡ Совпадение профиля: {top_match}%</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "📈 Career Prediction":
    st.title("📈 Career Prediction")
    st.write("Топ профессий на основе твоего текущего уровня (Figma, HTML/CSS, Hospitality).")
    
    if data and "top_3_jobs" in data:
        cols = st.columns(3)
        for i, job in enumerate(data["top_3_jobs"][:3]):
            with cols[i]:
                st.markdown(f"""
                <div class="job-card" style="height: 100%;">
                    <h3 style="color: #00ffcc; font-size: 1.3rem;">#{i+1} {job['title']}</h3>
                    <h2 style="color: #ffffff;">{job['match_percent']}%</h2>
                    <p style="color: #b366ff; font-size: 0.9rem; margin-top:15px; margin-bottom:5px;"><b>Missing Skills:</b></p>
                    <ul style="color: #a0a0a0; padding-left: 20px; font-size: 0.9rem;">
                        {''.join([f"<li>{skill}</li>" for skill in data.get("priority_skills_to_learn", ["Godot", "JS", "Animation"])])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Нет данных из career_prediction.json")
        
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🔄 Обновить прогноз"):
        st.cache_data.clear()
        st.rerun()

elif page == "⚖️ Balance Wheel":
    st.title("⚖️ Balance Wheel (Skills Radar)")
    st.write("Анализ распределения твоих Hard и Soft навыков.")
    
    categories = [
        'Figma', 'UI/UX Design', 'Godot', 'HTML/CSS', 'Adobe Illustrator', 'Prototyping', 
        'Teamwork', 'Communication', 'Responsibility', 'Problem Solving', 'Creativity'    
    ]
    
    hard_vals = [90, 75, 60, 70, 85, 80, None, None, None, None, None]
    soft_vals = [None, None, None, None, None, None, 85, 80, 90, 70, 75]
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=hard_vals,
        theta=categories,
        fill='toself',
        name='🛠️ Hard Skills',
        line_color='#00ffcc',
        fillcolor='rgba(0, 255, 204, 0.4)',
        connectgaps=False 
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=soft_vals,
        theta=categories,
        fill='toself',
        name='🧠 Soft Skills',
        line_color='#b366ff',
        fillcolor='rgba(179, 102, 255, 0.4)',
        connectgaps=False
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='rgba(255, 255, 255, 0.5)',
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                color='white',
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=13),
        margin=dict(l=60, r=60, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif page == "🌳 RPG Tech Tree":
    st.title("🌳 RPG Tech Tree")
    st.write("---")
    st.warning("🚧 **Раздел в разработке...** 🚧\n\nСкоро здесь будет интерактивное дерево навыков с прокачкой уровней!")

elif page == "💬 Live Coach":
    st.title("💬 Live Coach (Powered by Groq)")
    st.write("Твой личный AI-карьерный двойник. Спрашивай о планах, навыках или попроси 'Roast'!")
    
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    SYSTEM_PROMPT = """Ты — Digital Twin Career Engine Актана Кадыркулова. Ты его личный AI-карьерный коуч и цифровой двойник. 
Ты знаешь всё о нём: студент IT в Alatoo University, работает барменом, сильные навыки в Figma, UI/UX, Adobe Illustrator, есть интерес к Godot и анимациям. 
Отвечай дружелюбно, мотивирующе, честно и с практическими советами. 
Если пользователь просит roast — переходи в жёсткий, но мотивирующий тон."""

    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = [
            {"role": "assistant", "content": "Привет, Актан! Я твой Digital Twin Career Engine (теперь на базе Groq 🧠). Знаю твои крутые навыки в Figma и HTML/CSS, и твой опыт работы в баре. Давай строить твою Tech-карьеру! О чем поговорим сегодня?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Напиши своему коучу..."):
        if "groq_api_key" not in st.session_state or not st.session_state.groq_api_key:
            st.error("⚠️ Пожалуйста, введи свой Groq API Key в боковой панели (Sidebar) слева!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            try:
                client = Groq(api_key=st.session_state.groq_api_key)
                
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                    
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    stream = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=api_messages,
                        stream=True,
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Произошла ошибка при обращении к Groq API: {e}")

elif page == "🔥 Roast My Stack":
    st.title("🔥 Roast My Stack")
    st.write("Нажми на кнопку, если чувствуешь, что застрял и тебе нужен мощный пинок реальности.")
    
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("🚨 Roast Me! 🚨"):
        st.markdown("""
        <div class="roast-box">
            <h3>🔥 ТЕХЛИД ВОШЕЛ В ЧАТ 🔥</h3>
            <p>"Актан, ты до сих пор главный бармен и думаешь, что Figma — это уже профессия? 😂 
            Пора уже Godot подтянуть, а то так и будешь меню для кофеен рисовать всю жизнь. 
            Твои Soft-скиллы прокачаны на сотку — ты отлично общаешься с клиентами за стойкой, но машинам плевать на твою харизму, им нужен код! 
            Открывай редактор и начинай коммитить, иначе твой 'Digital Twin' уйдет работать в Tech быстрее тебя!"</p>
        </div>
        """, unsafe_allow_html=True)
