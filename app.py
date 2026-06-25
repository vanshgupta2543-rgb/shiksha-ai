import streamlit as st
import base64
from stt import transcribe
from tts import speak
from llm import simplify_concept, generate_quiz, evaluate_answer

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Shiksha AI",
    page_icon="🪔",
    layout="wide"
)

# ── Design System ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Baloo+2:wght@400;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: #0E0B2C;
    color: #F5F0E8;
}
.stApp { background-color: #0E0B2C; }

/* ── Header ── */
.shiksha-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 24px 0 8px 0;
}
.shiksha-title {
    font-family: 'Baloo 2', cursive;
    font-size: 42px;
    font-weight: 700;
    color: #FF9933;
    line-height: 1;
    margin: 0;
}
.shiksha-subtitle {
    font-size: 15px;
    color: #9B95C9;
    margin: 0;
    letter-spacing: 0.5px;
}
.divider {
    height: 2px;
    background: linear-gradient(90deg, #FF9933 0%, #2DD4BF 50%, transparent 100%);
    border: none;
    margin: 12px 0 24px 0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #1A1640;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #9B95C9;
    border-radius: 8px;
    font-size: 17px;
    font-weight: 600;
    padding: 10px 24px;
}
.stTabs [aria-selected="true"] {
    background: #FF9933 !important;
    color: #0E0B2C !important;
}

/* ── Cards ── */
.concept-card {
    background: #1A1640;
    border-radius: 20px;
    padding: 32px;
    margin: 16px 0;
    border: 1.5px solid #2A2460;
    box-shadow: 0 0 32px rgba(255,153,51,0.08);
    animation: fadeSlideIn 0.5s ease;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chalk-text {
    font-family: 'Baloo 2', cursive;
    font-size: 26px;
    color: #F5F0E8;
    line-height: 1.65;
    letter-spacing: 0.2px;
}
.hindi-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,153,51,0.15);
    border: 1px solid #FF9933;
    color: #FF9933;
    border-radius: 24px;
    padding: 5px 16px;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 16px;
}
.emoji-display {
    font-size: 72px;
    text-align: center;
    padding: 12px 0;
    filter: drop-shadow(0 0 12px rgba(255,153,51,0.3));
}
.key-point {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    background: rgba(45,212,191,0.08);
    border-left: 4px solid #2DD4BF;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 19px;
    color: #E0FDF9;
    font-weight: 600;
}

/* ── Quiz ── */
.quiz-card {
    background: #1A1640;
    border-radius: 20px;
    padding: 32px;
    margin: 16px 0;
    border: 1.5px solid #2A2460;
    animation: fadeSlideIn 0.4s ease;
}
.question-text {
    font-family: 'Baloo 2', cursive;
    font-size: 26px;
    color: #F5F0E8;
    line-height: 1.5;
    margin-bottom: 20px;
}
.option-pill {
    background: #12103A;
    border: 1.5px solid #2A2460;
    border-radius: 12px;
    padding: 13px 20px;
    margin: 8px 0;
    font-size: 19px;
    color: #C4BFEC;
    font-weight: 600;
    transition: all 0.2s;
}
.result-correct {
    background: rgba(45,212,191,0.12);
    border: 1.5px solid #2DD4BF;
    border-radius: 16px;
    padding: 20px 24px;
    font-size: 22px;
    color: #2DD4BF;
    font-weight: 700;
    animation: fadeSlideIn 0.4s ease;
}
.result-wrong {
    background: rgba(251,113,133,0.12);
    border: 1.5px solid #FB7185;
    border-radius: 16px;
    padding: 20px 24px;
    font-size: 22px;
    color: #FB7185;
    font-weight: 700;
    animation: fadeSlideIn 0.4s ease;
}
.score-card {
    background: linear-gradient(135deg, #1A1640, #0E1A40);
    border: 2px solid #FF9933;
    border-radius: 20px;
    padding: 36px;
    text-align: center;
    animation: fadeSlideIn 0.5s ease;
}
.score-number {
    font-family: 'Baloo 2', cursive;
    font-size: 64px;
    color: #FF9933;
    font-weight: 700;
    line-height: 1;
}
.score-label {
    font-size: 20px;
    color: #9B95C9;
    margin-top: 8px;
}

/* ── Inputs ── */
.stTextInput input {
    background: #1A1640 !important;
    border: 1.5px solid #2A2460 !important;
    border-radius: 10px !important;
    color: #F5F0E8 !important;
    font-size: 17px !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus {
    border-color: #FF9933 !important;
    box-shadow: 0 0 0 2px rgba(255,153,51,0.2) !important;
}

/* ── Buttons ── */
.stButton button {
    background: #FF9933 !important;
    color: #0E0B2C !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    width: 100%;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: #FFB347 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(255,153,51,0.3) !important;
}

/* ── Section labels ── */
.section-label {
    font-size: 13px;
    font-weight: 700;
    color: #9B95C9;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] { padding: 0 4px; }
</style>
""", unsafe_allow_html=True)

# ── Audio autoplay ────────────────────────────────────────────
def autoplay_audio(audio_bytes: bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="shiksha-header">
    <div>
        <p class="shiksha-title">🪔 Shiksha AI</p>
        <p class="shiksha-subtitle">Haryana Government School · Voice-Enabled AI Teaching Co-pilot</p>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["💡  Concept Samjhao", "📝  Voice Quiz"])

# ════════════════════════════════════════════════════════════════
# TAB 1 — CONCEPT SIMPLIFIER
# ════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 1.4], gap="large")

    with col1:
        st.markdown('<p class="section-label">Topic chunein</p>', unsafe_allow_html=True)
        audio = st.audio_input("🎤 Mic se bolo", key="concept_audio")
        text_input = st.text_input("", placeholder="Ya yahan type karein — e.g. Photosynthesis", label_visibility="collapsed")
        explain_btn = st.button("✨ Samjhao", key="explain_btn")

        st.markdown("""
        <div style="margin-top:24px; padding:16px; background:#1A1640; border-radius:12px; border:1px dashed #2A2460;">
            <p style="color:#9B95C9; font-size:14px; margin:0; line-height:1.6;">
                💬 <b style="color:#FF9933;">Kaise use karein:</b><br>
                Mic se concept bolo ya type karein.<br>
                AI Hinglish mein samjhayega aur board pe dikhayega.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if explain_btn:
            topic = ""
            if audio:
                with st.spinner("Sun raha hoon..."):
                    topic = transcribe(audio.read())
                st.markdown(f'<p style="color:#9B95C9; font-size:15px;">🎤 Suna: <i>{topic}</i></p>', unsafe_allow_html=True)
            elif text_input:
                topic = text_input

            if topic:
                with st.spinner("Samjha raha hoon..."):
                    result = simplify_concept(topic)

                emoji    = result.get("emoji_visual", "📚")
                explanation_hinglish = result.get("explanation_hinglish", "")
                explanation = explanation_hinglish  # kept for fallback compatibility
                key_points  = result.get("key_points", [])
                hindi_word  = result.get("hindi_word", "")

                explanation_hinglish = result.get("explanation_hinglish", "")
                subtitles = result.get("subtitles", [])

                st.markdown(f'<div class="emoji-display">{emoji}</div>', unsafe_allow_html=True)

                if hindi_word:
                    st.markdown(f'<span class="hindi-badge">📖 {hindi_word}</span>', unsafe_allow_html=True)

                # Start TTS immediately
                with st.spinner("Bol raha hoon..."):
                    audio_out = speak(explanation_hinglish)
                    autoplay_audio(audio_out)

                # Rolling side-by-side subtitles in sync with speech
                subtitle_placeholder = st.empty()
                import time

                words_per_second = 2.5
                for i, sub in enumerate(subtitles):
                    en = sub.get("english", "")
                    hi = sub.get("hindi", "")
                    word_count = len(explanation_hinglish.split()) / max(len(subtitles), 1)
                    display_duration = max(word_count / words_per_second, 2.0)

                    subtitle_placeholder.markdown(f"""
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:8px 0;">
                            <div class="concept-card" style="padding:20px;">
                                <p style="color:#9B95C9; font-size:12px; font-weight:700; letter-spacing:1px; margin-bottom:8px;">ENGLISH</p>
                                <div class="chalk-text" style="font-size:21px;">{en}</div>
                            </div>
                            <div class="concept-card" style="padding:20px; border-color:#FF9933;">
                                <p style="color:#FF9933; font-size:12px; font-weight:700; letter-spacing:1px; margin-bottom:8px;">हिंदी</p>
                                <div style="font-size:22px; color:#FFD580; font-family:'Baloo 2',cursive; line-height:1.6;">{hi}</div>
                            </div>
                        </div>
                        <div style="background:#1A1640; border-radius:99px; height:4px; margin-top:4px;">
                            <div style="background:linear-gradient(90deg,#FF9933,#2DD4BF); width:{int(((i+1)/len(subtitles))*100)}%; height:4px; border-radius:99px;"></div>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(display_duration)

                # After subtitles finish — show full explanation as reference
                subtitle_placeholder.markdown(f"""
                    <div class="concept-card">
                        <p style="color:#9B95C9; font-size:12px; font-weight:700; letter-spacing:1px; margin-bottom:12px;">FULL EXPLANATION</p>
                        <div class="chalk-text">{explanation_hinglish}</div>
                    </div>
                """, unsafe_allow_html=True)

                if key_points:
                    st.markdown('<p class="section-label" style="margin-top:20px;">Key Points</p>', unsafe_allow_html=True)
                    for pt in key_points:
                        st.markdown(f'<div class="key-point">✅ {pt}</div>', unsafe_allow_html=True)

            elif explain_btn:
                st.warning("Pehle topic bolo ya type karein.")
        else:
            st.markdown("""
            <div style="height:300px; display:flex; align-items:center; justify-content:center; flex-direction:column; gap:12px; opacity:0.4;">
                <div style="font-size:56px;">🖊️</div>
                <p style="color:#9B95C9; font-size:17px;">Explanation yahan dikhegi</p>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — VOICE QUIZ
# ════════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns([1, 1.6], gap="large")

    with col1:
        st.markdown('<p class="section-label">Quiz Setup</p>', unsafe_allow_html=True)
        quiz_audio = st.audio_input("🎤 Topic bolo", key="quiz_audio")
        quiz_topic = st.text_input("", placeholder="Ya type karein — e.g. Solar System", label_visibility="collapsed", key="quiz_topic")
        num_q = st.slider("Kitne questions?", 2, 5, 3)
        generate_btn = st.button("🎯 Quiz Shuru Karo", key="generate_btn")

        if generate_btn:
            resolved_topic = ""
            if quiz_audio:
                with st.spinner("Sun raha hoon..."):
                    resolved_topic = transcribe(quiz_audio.read())
                st.markdown(f'<p style="color:#9B95C9; font-size:15px;">🎤 Suna: <i>{resolved_topic}</i></p>', unsafe_allow_html=True)
            elif quiz_topic:
                resolved_topic = quiz_topic

            if resolved_topic:
                with st.spinner("Quiz ban rahi hai..."):
                    quiz_data = generate_quiz(resolved_topic, num_q)
                    st.session_state["quiz"]    = quiz_data.get("questions", [])
                    st.session_state["q_index"] = 0
                    st.session_state["score"]   = 0
            else:
                st.warning("Pehle topic bolo ya type karein.")

        st.markdown("""
        <div style="margin-top:24px; padding:16px; background:#1A1640; border-radius:12px; border:1px dashed #2A2460;">
            <p style="color:#9B95C9; font-size:14px; margin:0; line-height:1.6;">
                💬 <b style="color:#FF9933;">Quiz kaise chalein:</b><br>
                1. Topic aur questions choose karein<br>
                2. Question board pe dikhega<br>
                3. Student mic se ya type karke jawab de<br>
                4. AI turant evaluate karega
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if "quiz" in st.session_state and st.session_state["quiz"]:
            questions = st.session_state["quiz"]
            idx       = st.session_state.get("q_index", 0)
            total     = len(questions)

            # Progress bar
            progress = idx / total
            st.markdown(f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#9B95C9; font-size:14px; font-weight:700;">PROGRESS</span>
                    <span style="color:#FF9933; font-size:14px; font-weight:700;">{idx}/{total}</span>
                </div>
                <div style="background:#1A1640; border-radius:99px; height:8px;">
                    <div style="background:linear-gradient(90deg,#FF9933,#2DD4BF); width:{int(progress*100)}%; height:8px; border-radius:99px; transition:width 0.4s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if idx < total:
                q = questions[idx]
                st.markdown(f"""
                <div class="quiz-card">
                    <p style="color:#FF9933; font-size:13px; font-weight:700; letter-spacing:1px; margin-bottom:8px;">QUESTION {idx+1}</p>
                    <div class="question-text">{q["q"]}</div>
                    {''.join(f'<div class="option-pill">{opt}</div>' for opt in q["options"])}
                </div>
                """, unsafe_allow_html=True)

                bcol1, bcol2 = st.columns(2)
                with bcol1:
                    if st.button("🔊 Question Sunao", key=f"tts_{idx}"):
                        announcement = f"Question {idx+1}. {q['q']}. Options hain: {', '.join(q['options'])}"
                        autoplay_audio(speak(announcement))

                st.markdown('<p class="section-label" style="margin-top:16px;">Student ka Jawab</p>', unsafe_allow_html=True)
                answer_audio = st.audio_input("🎤 Mic se jawab do", key=f"answer_{idx}")
                answer_text  = st.text_input("", placeholder="Ya type karo: A, B, C, ya D", key=f"text_{idx}", label_visibility="collapsed")
                submit_btn   = st.button("✅ Submit", key=f"submit_{idx}")

                if submit_btn:
                    student_ans = ""
                    if answer_audio:
                        with st.spinner("Jawab sun raha hoon..."):
                            student_ans = transcribe(answer_audio.read())
                        st.markdown(f'<p style="color:#9B95C9; font-size:15px;">🎤 Suna: <i>{student_ans}</i></p>', unsafe_allow_html=True)
                    elif answer_text:
                        student_ans = answer_text

                    if student_ans:
                        with st.spinner("Check kar raha hoon..."):
                            eval_result = evaluate_answer(q["q"], q["answer"], student_ans)

                        correct     = eval_result.get("correct", False)
                        feedback    = eval_result.get("feedback", "")
                        explanation = q.get("explanation", "")

                        if correct:
                            st.markdown(f'<div class="result-correct">✅ Bilkul sahi! {feedback}</div>', unsafe_allow_html=True)
                            st.session_state["score"] += 1
                        else:
                            st.markdown(f'<div class="result-wrong">❌ Galat. Sahi jawab: <b>{q["answer"]}</b> — {explanation}</div>', unsafe_allow_html=True)

                        autoplay_audio(speak(feedback))
                        st.session_state["q_index"] += 1
                        st.rerun()

            else:
                score = st.session_state.get("score", 0)
                pct   = int((score / total) * 100)

                if pct == 100:
                    msg   = "Waah! Perfect score! Aap bahut hoshiyaar hain! 🌟"
                    color = "#FF9933"
                elif pct >= 60:
                    msg   = f"Achha kiya! {score} out of {total} sahi. Thodi aur practice karo!"
                    color = "#2DD4BF"
                else:
                    msg   = f"Koi baat nahi! {score} sahi the. Dobara padho aur try karo — you've got this!"
                    color = "#FB7185"

                st.markdown(f"""
                <div class="score-card">
                    <div class="score-number" style="color:{color};">{score}/{total}</div>
                    <div class="score-label">{msg}</div>
                </div>
                """, unsafe_allow_html=True)

                autoplay_audio(speak(msg))

                if st.button("🔄 Nayi Quiz Shuru Karo"):
                    for key in ["quiz", "q_index", "score"]:
                        st.session_state.pop(key, None)
                    st.rerun()
        else:
            st.markdown("""
            <div style="height:300px; display:flex; align-items:center; justify-content:center; flex-direction:column; gap:12px; opacity:0.4;">
                <div style="font-size:56px;">📋</div>
                <p style="color:#9B95C9; font-size:17px;">Quiz yahan dikhegi</p>
            </div>
            """, unsafe_allow_html=True)