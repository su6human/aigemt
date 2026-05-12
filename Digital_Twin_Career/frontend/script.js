document.addEventListener('DOMContentLoaded', () => {
    
    // --- Navigation Logic ---
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.page-section');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');

            if (targetId === 'radar') {
                renderRadarChart();
            }
        });
    });

    // --- Fetch Data ---
    // Since we are serving static files from FastAPI, API is at the same origin
    const API_BASE = window.location.origin;

    async function loadPredictionData() {
        try {
            const res = await fetch(`${API_BASE}/api/prediction`);
            const data = await res.json();
            
            // Update Home
            if (data.top_3_jobs && data.top_3_jobs.length > 0) {
                const topJob = data.top_3_jobs[0];
                document.getElementById('home-top-job').innerHTML = `
                    <h2 class="job-title">🎮 ${topJob.title}</h2>
                    <p class="job-desc">Идеальное сочетание твоих навыков дизайна и интереса к интерактивам/играм.</p>
                    <p class="job-match">⚡ Совпадение профиля: ${topJob.match_percent}%</p>
                `;
            }

            // Update Prediction Grid
            if (data.top_3_jobs) {
                const grid = document.getElementById('prediction-grid');
                grid.innerHTML = '';
                
                const missingSkillsHtml = data.priority_skills_to_learn 
                    ? data.priority_skills_to_learn.map(s => `<li>🔴 ${s}</li>`).join('')
                    : '<li>Нет данных</li>';

                data.top_3_jobs.forEach((job, index) => {
                    grid.innerHTML += `
                        <div class="job-card">
                            <h3 class="job-title">#${index + 1} ${job.title}</h3>
                            <h2 style="color: #fff; margin-bottom: 15px;">${job.match_percent}%</h2>
                            <p class="missing-skills">Missing Skills:</p>
                            <ul class="missing-skills-list">${missingSkillsHtml}</ul>
                        </div>
                    `;
                });
            }
        } catch (error) {
            console.error("Failed to load predictions", error);
            document.getElementById('home-top-job').innerHTML = '<p style="color:red;">Ошибка загрузки данных</p>';
            document.getElementById('prediction-grid').innerHTML = '<p style="color:red;">Ошибка загрузки данных</p>';
        }
    }

    loadPredictionData();
    document.getElementById('refresh-prediction').addEventListener('click', loadPredictionData);

    // --- Radar Chart ---
    let radarRendered = false;
    async function renderRadarChart() {
        if (radarRendered) return;
        
        try {
            const res = await fetch(`${API_BASE}/api/skills`);
            const data = await res.json();

            const hardTrace = {
                type: 'scatterpolar',
                r: [...data.hard_skills, data.hard_skills[0]],
                theta: [...data.categories, data.categories[0]],
                fill: 'toself',
                name: '🛠️ Hard Skills',
                line: { color: '#00ffcc' },
                fillcolor: 'rgba(0, 255, 204, 0.4)'
            };

            const softTrace = {
                type: 'scatterpolar',
                r: [...data.soft_skills, data.soft_skills[0]],
                theta: [...data.categories, data.categories[0]],
                fill: 'toself',
                name: '🧠 Soft Skills',
                line: { color: '#b366ff' },
                fillcolor: 'rgba(179, 102, 255, 0.4)'
            };

            const layout = {
                polar: {
                    radialaxis: { visible: true, range: [0, 100], color: 'rgba(255,255,255,0.5)', gridcolor: 'rgba(255,255,255,0.1)' },
                    angularaxis: { color: 'white', gridcolor: 'rgba(255,255,255,0.1)' },
                    bgcolor: 'rgba(0,0,0,0)'
                },
                showlegend: true,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: 'white', size: 13 },
                margin: { l: 60, r: 60, t: 40, b: 40 }
            };

            Plotly.newPlot('radar-chart', [hardTrace, softTrace], layout, {responsive: true});
            radarRendered = true;
        } catch (e) {
            console.error("Failed to load radar data", e);
        }
    }

    // --- Chat Logic ---
    let chatMessages = [
        { role: 'assistant', content: 'Привет, Актан! Я твой Digital Twin Career Engine (Backend API). Знаю твои крутые навыки в Figma и HTML/CSS, и твой опыт работы в баре. Давай строить твою Tech-карьеру! О чем поговорим сегодня?' }
    ];

    const chatBox = document.getElementById('chat-box');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-chat');

    function renderChat() {
        chatBox.innerHTML = '';
        chatMessages.forEach(msg => {
            const div = document.createElement('div');
            div.className = `chat-message ${msg.role === 'user' ? 'msg-user' : 'msg-assistant'}`;
            const header = msg.role === 'user' ? '👤 Актан' : '🤖 Digital Twin Coach';
            
            // Simple markdown parser for bold/italic/newlines
            let text = msg.content
                .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                .replace(/\*(.*?)\*/g, '<i>$1</i>')
                .replace(/\n/g, '<br>');

            div.innerHTML = `<div class="msg-header">${header}</div><div>${text}</div>`;
            chatBox.appendChild(div);
        });
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    renderChat();

    clearBtn.addEventListener('click', () => {
        chatMessages = [chatMessages[0]];
        renderChat();
    });

    async function sendMessage() {
        const text = chatInput.value.trim();
        const apiKey = document.getElementById('groq-api-key').value.trim();

        if (!text) return;
        if (!apiKey) {
            alert("⚠️ Пожалуйста, введи свой Groq API Key в боковой панели (Слева)!");
            return;
        }

        // Add user msg
        chatMessages.push({ role: 'user', content: text });
        chatInput.value = '';
        renderChat();

        // Show loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'chat-message msg-assistant';
        loadingDiv.innerHTML = '<i>Коуч печатает...</i>';
        chatBox.appendChild(loadingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const res = await fetch(`${API_BASE}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: chatMessages,
                    api_key: apiKey
                })
            });

            const data = await res.json();
            
            // Remove loading
            chatBox.removeChild(loadingDiv);

            if (res.ok) {
                chatMessages.push({ role: 'assistant', content: data.response });
            } else {
                chatMessages.push({ role: 'assistant', content: `❌ Ошибка: ${data.detail}` });
            }
        } catch (e) {
            chatBox.removeChild(loadingDiv);
            chatMessages.push({ role: 'assistant', content: `❌ Сетевая ошибка при обращении к серверу.` });
        }

        renderChat();
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
