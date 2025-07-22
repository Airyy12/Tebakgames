# === app.py ===
import streamlit as st
from exp_manager import ExpManager
from question_manager import QuestionManager
from quiz_session import QuizSession

st.title("🎓 Quiz Adaptif Berbasis EXP + AI Penjelasan")

if 'quiz' not in st.session_state:
    exp_manager = ExpManager()
    question_manager = QuestionManager("questions.json")
    st.session_state.quiz = QuizSession(exp_manager, question_manager)

quiz = st.session_state.quiz

status = quiz.get_status()

st.markdown(f"**Level:** {status['level']} | **EXP:** {status['exp']} | 🔥 Streak: {status['streak']}")

if status['current_question'] is None:
    question = quiz.get_next_question()
else:
    question = status['current_question']

st.subheader(f"📘 Soal Level {question['level']}:")
st.markdown(f"**{question['question']}**")

form = st.form(key="quiz_form")
selected = form.radio("Pilih jawaban:", question["options"])
submit = form.form_submit_button("Jawab")

if submit:
    result = quiz.answer_question(selected)

    if result["is_correct"]:
        st.success("✅ Jawaban benar!")
    else:
        st.error(f"❌ Salah! Jawaban yang benar: **{result['correct_answer']}**")
        st.markdown(f"**Penjelasan AI:** {result['explanation']}")

    st.markdown(f"**EXP + {result['exp_change']}**")
    if result["level_after"] > result["level_before"]:
        st.balloons()
        st.success(f"🎉 Naik ke Level {result['level_after']}!")

    if st.button("Lanjut Soal Berikutnya"):
        quiz.get_next_question()
        st.rerun()