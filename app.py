import streamlit as st
import exp_manager
from question_manager import QuestionManager
from quiz_session import QuizSession

st.title("🎓 Quiz Adaptif Berbasis EXP + AI")

# Inisialisasi sesi
if 'quiz' not in st.session_state:
    question_manager = QuestionManager("questions.json")
    st.session_state.quiz = QuizSession(exp_manager, question_manager)
    st.session_state.show_result = False  # untuk kontrol tampilan hasil

quiz = st.session_state.quiz
status = quiz.get_status()

st.markdown(f"**Level:** {status['level']} | **EXP:** {status['exp']} | 🔥 Streak: {status['streak']}")

# Ambil soal jika belum ada atau jika lanjut ditekan
if status['current_question'] is None or not st.session_state.get("show_result", False):
    question = quiz.get_next_question()
else:
    question = status['current_question']

# Tampilkan soal
st.subheader(f"📘 Soal Level {question['level']} - {question['category']} ({question['difficulty'].capitalize()})")
st.markdown(f"**{question['question']}**")

form = st.form(key="quiz_form", clear_on_submit=True)
selected = form.radio("Pilih jawaban:", question["options"])
submit = form.form_submit_button("Jawab")

# Proses jawaban
if submit:
    result = quiz.answer_question(selected)
    st.session_state.show_result = True  # tampilkan hasil setelah jawab

    if result["is_correct"]:
        st.success("✅ Jawaban benar!")
    else:
        st.error(f"❌ Salah! Jawaban yang benar: **{result['correct_answer']}**")
        st.markdown(f"**Penjelasan AI:** {result['explanation']}**")

    st.markdown(f"**EXP {'+' if result['exp_change'] >= 0 else ''}{result['exp_change']}**")

    if result["level_after"] > result["level_before"]:
        st.balloons()
        st.success(f"🎉 Naik ke Level {result['level_after']}!")

# Tombol lanjut hanya muncul setelah menjawab
if st.session_state.get("show_result", False):
    if st.button("➡️ Lanjut Soal Berikutnya"):
        quiz.get_next_question()
        st.session_state.show_result = False
        st.rerun()
