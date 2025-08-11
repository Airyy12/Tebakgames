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
        <img src="https://img.icons8.com/color/96/000000/graduation-cap.png" width="56" style="border-radius:50%;box-shadow:0 2px 8px #0003;"/>
        <h1 style="margin-bottom:0;color:#2e7dff;">Quiz Adaptif <span style="color:#ffb300;">EXP</span></h1>
    </div>
    """,
    unsafe_allow_html=True
)

if "username" not in st.session_state:
    st.session_state.username = None

# --- Sidebar: User Info, Menu, & Logout ---
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;">
            <img src="https://img.icons8.com/color/96/000000/user-male-circle--v2.png" width="80" style="border-radius:50%;box-shadow:0 2px 8px #0003;"/>
        </div>
        """, unsafe_allow_html=True
    )
    if st.session_state.username:
        st.markdown(f"<div style='text-align:center;font-size:1.1em;'><b>👤 {st.session_state.username}</b></div>", unsafe_allow_html=True)
        sidebar_menu = st.radio(
            "Menu",
            ["🏆 Quiz", "🧑‍💻 Profil Player", "ℹ️ Penjelasan Aplikasi"]
        )
        st.markdown("---")
        if st.button("🚪 Logout"):
            for k in ["username", "quiz", "quiz_user", "current_question", "show_result", "last_result"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()
    else:
        sidebar_menu = st.radio("Menu", ["🔑 Login", "📝 Register", "ℹ️ Penjelasan Aplikasi"])
        st.markdown("<div style='text-align:center;color:#d7263d;font-weight:bold;'>Silakan login/register dulu</div>", unsafe_allow_html=True)

# --- Login/Register/Penjelasan Section (sebelum login) ---
if st.session_state.username is None:
    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.3em;font-weight:bold;color:#2e7dff;'>Login / Register</div>", unsafe_allow_html=True)
    st.markdown("---")
    if sidebar_menu == "🔑 Login":
        with st.form(key="login_form", clear_on_submit=False):
            st.markdown("<div style='font-size:1.1em;font-weight:bold;'>Masuk ke akun kamu</div>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("🔓 Login", use_container_width=True)
            if submit:
                ok, msg = authenticate_user(username, password)
                if ok:
                    st.session_state.username = username
                    st.success("Login berhasil!")
                    st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()
                else:
                    st.error(msg)
    elif sidebar_menu == "📝 Register":
        st.markdown("<div style='font-size:1.1em;font-weight:bold;'>Buat akun baru</div>", unsafe_allow_html=True)
        username = st.text_input("Username (baru)")
        password = st.text_input("Password (baru)", type="password")
        if st.button("📝 Register", use_container_width=True):
            ok, msg = register_user(username, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    elif sidebar_menu == "ℹ️ Penjelasan Aplikasi":
        st.header("ℹ️ Penjelasan Aplikasi")
        st.markdown("""
        <div style="background:#23272f;border-radius:16px;padding:24px 20px;margin-bottom:16px;box-shadow:0 2px 12px #0003;">
        <h3 style="color:#2e7dff;">Tentang Quiz Adaptif EXP+AI</h3>
        <p>Quiz Adaptif EXP+AI adalah aplikasi kuis edukasi yang menyesuaikan tingkat kesulitan soal berdasarkan performa dan pengalaman (EXP) pemain.</p>
        <h4 style="color:#ffb300;">📜 Peraturan Permainan</h4>
        <ul>
        <li>🔑 <b>Login/Register:</b> Setiap pemain harus login atau mendaftar sebelum bermain.</li>
        <li>🗂️ <b>Satu Akun Satu Progress:</b> Progress (level, exp, streak) disimpan per akun.</li>
        <li>🚫 <b>Tidak Boleh Curang:</b> Dilarang menggunakan bantuan eksternal untuk menjawab soal.</li>
        </ul>
        <h4 style="color:#ffb300;">⚙️ Mekanisme Permainan</h4>
        <ul>
        <li>🏅 <b>Level & EXP:</b> Mulai dari level 1 dan EXP 0. Jawaban benar menambah EXP, jika EXP cukup maka naik level.</li>
        <li>🔥 <b>Streak:</b> Bertambah jika menjawab benar berturut-turut, direset jika salah.</li>
        <li>🧠 <b>Soal Adaptif:</b> Soal menyesuaikan level dan performa pemain.</li>
        <li>✅ <b>Jawaban:</b> Pilih salah satu jawaban, hasil langsung ditampilkan.</li>
        <li>✨ <b>EXP & Level Up:</b> Jawaban benar menambah EXP, jawaban salah bisa mengurangi EXP (tergantung level).</li>
        <li>💾 <b>Progress Tersimpan:</b> Otomatis tersimpan setiap selesai menjawab soal.</li>
        <li>🏆 <b>Level Maksimum:</b> Jika sudah maksimum, quiz selesai dan tunggu update berikutnya.</li>
        </ul>
        <h4 style="color:#ffb300;">💡 Tips</h4>
        <ul>
        <li>Jawab dengan teliti agar streak dan EXP bertambah cepat.</li>
        <li>Logout dan lanjutkan progress kapan saja.</li>
        </ul>
        <div style="text-align:center;font-size:1.2em;color:#2e7dff;font-weight:bold;">Selamat bermain dan semoga sukses! 🎉</div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- Menu Penjelasan & Profil Player (setelah login) ---
if st.session_state.username and sidebar_menu == "ℹ️ Penjelasan Aplikasi":
    st.header("ℹ️ Penjelasan Aplikasi")
    st.markdown("""
    <div style="background:#23272f;border-radius:16px;padding:24px 20px;margin-bottom:16px;box-shadow:0 2px 12px #0003;">
    <h3 style="color:#2e7dff;">Tentang Quiz Adaptif EXP+AI</h3>
    <p>Quiz Adaptif EXP+AI adalah aplikasi kuis edukasi yang menyesuaikan tingkat kesulitan soal berdasarkan performa dan pengalaman (EXP) pemain.</p>
    <h4 style="color:#ffb300;">📜 Peraturan Permainan</h4>
    <ul>
    <li>🔑 <b>Login/Register:</b> Setiap pemain harus login atau mendaftar sebelum bermain.</li>
    <li>🗂️ <b>Satu Akun Satu Progress:</b> Progress (level, exp, streak) disimpan per akun.</li>
    <li>🚫 <b>Tidak Boleh Curang:</b> Dilarang menggunakan bantuan eksternal untuk menjawab soal.</li>
    </ul>
    <h4 style="color:#ffb300;">⚙️ Mekanisme Permainan</h4>
    <ul>
    <li>🏅 <b>Level & EXP:</b> Mulai dari level 1 dan EXP 0. Jawaban benar menambah EXP, jika EXP cukup maka naik level.</li>
    <li>🔥 <b>Streak:</b> Bertambah jika menjawab benar berturut-turut, direset jika salah.</li>
    <li>🧠 <b>Soal Adaptif:</b> Soal menyesuaikan level dan performa pemain.</li>
    <li>✅ <b>Jawaban:</b> Pilih salah satu jawaban, hasil langsung ditampilkan.</li>
    <li>✨ <b>EXP & Level Up:</b> Jawaban benar menambah EXP, jawaban salah bisa mengurangi EXP (tergantung level).</li>
    <li>💾 <b>Progress Tersimpan:</b> Otomatis tersimpan setiap selesai menjawab soal.</li>
    <li>🏆 <b>Level Maksimum:</b> Jika sudah maksimum, quiz selesai dan tunggu update berikutnya.</li>
    </ul>
    <h4 style="color:#ffb300;">💡 Tips</h4>
    <ul>
    <li>Jawab dengan teliti agar streak dan EXP bertambah cepat.</li>
    <li>Logout dan lanjutkan progress kapan saja.</li>
    </ul>
    <div style="text-align:center;font-size:1.2em;color:#2e7dff;font-weight:bold;">Selamat bermain dan semoga sukses! 🎉</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if st.session_state.username and sidebar_menu == "🧑‍💻 Profil Player":
    st.header("🧑‍💻 Profil Player")
    user_data = get_user_progress(st.session_state.username)
    st.markdown(f"""
    <div style="background:#23272f;border-radius:16px;padding:24px 20px;margin-bottom:16px;box-shadow:0 2px 12px #0003;">
    <div style="font-size:1.3em;font-weight:bold;color:#2e7dff;">👤 {st.session_state.username}</div>
    <div style="margin-top:8px;">
        <span style="font-size:1.1em;">🏅 <b>Level:</b> {user_data.get("level", 1)}</span><br>
        <span style="font-size:1.1em;">✨ <b>EXP:</b> {user_data.get("exp", 0)}</span><br>
        <span style="font-size:1.1em;">🔥 <b>Streak:</b> {user_data.get("streak", 0)}</span>
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Quiz Section (setelah login & menu Quiz) ---
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
    st.markdown(f"<div style='font-size:1.2em;background:#23272f;border-radius:8px;padding:8px 0;text-align:center;color:#ffb300;box-shadow:0 2px 8px #0002;'>🏅 <b>Level:</b> {status['level']}</div>", unsafe_allow_html=True)
with col2:
    next_level = status['level'] + 1
    exp_now = status['exp']
    exp_min = exp_manager.LEVEL_THRESHOLDS[status['level']]
    exp_max = exp_manager.LEVEL_THRESHOLDS.get(next_level, exp_now+100)
    denom = max(exp_max - exp_min, 1)
    exp_pct = (exp_now - exp_min) / denom
    exp_pct = min(max(exp_pct, 0.0), 1.0)
    st.markdown(f"<div style='font-size:1.1em;text-align:center;'><b>EXP:</b> {exp_now} / {exp_max}</div>", unsafe_allow_html=True)
    st.progress(exp_pct)
with col3:
    st.markdown(f"<div style='font-size:1.2em;background:#23272f;border-radius:8px;padding:8px 0;text-align:center;color:#d7263d;box-shadow:0 2px 8px #0002;'>🔥 <b>Streak:</b> {status['streak']}</div>", unsafe_allow_html=True)
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
        <div style="background:#23272f;border-radius:16px;padding:24px 20px;margin-bottom:16px;box-shadow:0 2px 12px #0003;">
            {html}
        </div>
        """, unsafe_allow_html=True
    )

if not st.session_state.get("show_result", False):
    card_box(
        f"<div style='font-size:1.2em;color:#2e7dff;'><b>📘 Soal Level {question['level']} - {question['category']} ({question['difficulty'].capitalize()})</b></div><br>"
        f"<span style='font-size:1.1em'>{question['question']}</span>"
    )
    form = st.form(key="quiz_form", clear_on_submit=True)
    selected = form.radio("Pilih jawaban:", question["options"])
    submit = form.form_submit_button("✅ Jawab", use_container_width=True)

    if submit:
        result = quiz.answer_question(selected)
        st.session_state.last_result = result
        st.session_state.show_result = True
        st.rerun()
else:
    result = st.session_state.last_result
    if result["is_correct"]:
        card_box("<div style='color:green;font-size:1.2em'><b>✅ Jawaban benar!</b></div>")
        st.markdown(f"<div style='font-size:1.1em;color:#2e7dff;'><b>EXP {'+' if result['exp_change'] >= 0 else ''}{result['exp_change']}</b></div>", unsafe_allow_html=True)
    else:
        card_box("<div style='color:#d7263d;font-size:1.2em'><b>❌ Jawaban salah!</b></div>")
        if result["exp_change"] < 0:
            st.markdown(f"<div style='font-size:1.1em;color:#d7263d;'><b>EXP {result['exp_change']}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:1.1em;color:#ffb300;'><b>EXP tidak berkurang di level ini.</b></div>", unsafe_allow_html=True)

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
    if st.button("➡️ Soal Berikutnya", use_container_width=True, key="next_question"):
        st.session_state.current_question = None
        st.session_state.show_result = False
        st.session_state.last_result = None
        st.rerun()
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
    if st.button("➡️ Soal Berikutnya", use_container_width=True, key="next_question_2"):
        st.session_state.current_question = None
        st.session_state.show_result = False
        st.session_state.last_result = None
        st.rerun()
