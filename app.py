import streamlit as st
import exp_manager
from question_manager import QuestionManager
from quiz_session import QuizSession
from user_manager import register_user, authenticate_user, get_user_progress, update_user_progress

st.set_page_config(page_title="Quiz Adaptif EXP+AI", page_icon="🎓", layout="centered")

# --- Header & Sidebar ---
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:16px;">
        <img src="https://img.icons8.com/color/96/000000/graduation-cap.png" width="48"/>
        <h1 style="margin-bottom:0;">Quiz Adaptif EXP</h1>
    </div>
    """,
    unsafe_allow_html=True
)

if "username" not in st.session_state:
    st.session_state.username = None

# --- Sidebar: User Info & Logout ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/user-male-circle--v2.png", width=80)
    if st.session_state.username:
        st.markdown(f"**👤 {st.session_state.username}**")
        if st.button("🚪 Logout"):
            for k in ["username", "quiz", "quiz_user", "current_question", "show_result", "last_result"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()
    else:
        st.markdown("**Silakan login/register dulu**")

# --- Login/Register Section ---
if st.session_state.username is None:
    menu = st.sidebar.radio("Menu", ["Login", "Register"])
    st.header("Login / Register")

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            ok, msg = authenticate_user(username, password)
            if ok:
                st.session_state.username = username
                st.success("Login berhasil!")
                st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()
            else:
                st.error(msg)
    else:
        username = st.text_input("Username (baru)")
        password = st.text_input("Password (baru)", type="password")
        if st.button("Register", use_container_width=True):
            ok, msg = register_user(username, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    st.stop()

# --- Quiz Section (setelah login) ---
username = st.session_state.username
user_data = get_user_progress(username)

# Inisialisasi sesi quiz per user
if 'quiz' not in st.session_state or st.session_state.get("quiz_user") != username:
    question_manager = QuestionManager("questions.json")
    quiz = QuizSession(exp_manager, question_manager)
    # Load progress user
    quiz.current_level = user_data.get("level", 1)
    quiz.current_exp = user_data.get("exp", 0)
    quiz.current_streak = user_data.get("streak", 0)
    st.session_state.quiz = quiz
    st.session_state.quiz_user = username
    st.session_state.current_question = None
    st.session_state.show_result = False
    st.session_state.last_result = None

quiz = st.session_state.quiz
status = quiz.get_status()

# --- Status Bar ---
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.markdown(f"<span style='font-size:1.2em'>🏅</span> <b>Level:</b> {status['level']}", unsafe_allow_html=True)
with col2:
    # Progress bar EXP
    next_level = status['level'] + 1
    exp_now = status['exp']
    exp_min = exp_manager.LEVEL_THRESHOLDS[status['level']]
    exp_max = exp_manager.LEVEL_THRESHOLDS.get(next_level, exp_now+100)
    # Ensure denominator is never zero
    denom = max(exp_max - exp_min, 1)
    exp_pct = (exp_now - exp_min) / denom
    exp_pct = min(max(exp_pct, 0.0), 1.0)  # Clamp between 0.0 and 1.0
    st.markdown(f"<b>EXP:</b> {exp_now} / {exp_max}", unsafe_allow_html=True)
    st.progress(exp_pct)
with col3:
    st.markdown(f"<span style='font-size:1.2em'>🔥</span> <b>Streak:</b> {status['streak']}", unsafe_allow_html=True)
st.markdown("---")

# --- Cek Level Maksimum ---
max_level = max(exp_manager.LEVEL_THRESHOLDS.keys())
if status['level'] >= max_level:
    st.success("🏆 Selamat! Anda telah mencapai level maksimum.")
    st.info("Quiz telah selesai. Silakan logout atau tunggu update soal/level berikutnya.")
    st.stop()

# --- Soal & Jawaban ---
if st.session_state.get("current_question") is None and not st.session_state.get("show_result", False):
    question = quiz.get_next_question()
    st.session_state.current_question = question
else:
    question = st.session_state.current_question

def card_box(html):
    st.markdown(
        f"""
        <div style="background:#23272f;border-radius:12px;padding:24px 20px;margin-bottom:16px;box-shadow:0 2px 8px #0002;">
            {html}
        </div>
        """, unsafe_allow_html=True
    )

if not st.session_state.get("show_result", False):
    card_box(
        f"<b>📘 Soal Level {question['level']} - {question['category']} ({question['difficulty'].capitalize()})</b><br><br>"
        f"<span style='font-size:1.1em'>{question['question']}</span>"
    )
    form = st.form(key="quiz_form", clear_on_submit=True)
    selected = form.radio("Pilih jawaban:", question["options"])
    submit = form.form_submit_button("Jawab", use_container_width=True)

    if submit:
        result = quiz.answer_question(selected)
        st.session_state.last_result = result
        st.session_state.show_result = True
        st.rerun()
else:
    result = st.session_state.last_result
    if result["is_correct"]:
        card_box("<span style='color:green;font-size:1.2em'><b>✅ Jawaban benar!</b></span>")
        st.markdown(f"**EXP {'+' if result['exp_change'] >= 0 else ''}{result['exp_change']}**")
    else:
        card_box("<span style='color:#d7263d;font-size:1.2em'><b>❌ Jawaban salah!</b></span>")
        if result["exp_change"] < 0:
            st.markdown(f"**EXP {result['exp_change']}**")
        else:
            st.markdown("**EXP tidak berkurang di level ini.**")

    if result["level_after"] > result["level_before"]:
        st.balloons()
        st.success(f"🎉 Naik ke Level {result['level_after']}!")

    # Simpan progress user setiap selesai menjawab
    update_user_progress(
        username,
        quiz.current_level,
        quiz.current_exp,
        quiz.current_streak
    )

    # Tombol untuk lanjut ke soal berikutnya
    st.markdown("---")
    if st.button("➡️ Soal Berikutnya", use_container_width=True):
        st.session_state.current_question = None
        st.session_state.show_result = False
        st.session_state.last_result = None
        st.rerun()
