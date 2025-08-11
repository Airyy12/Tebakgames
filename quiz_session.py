import os
import exp_manager
from dotenv import load_dotenv

load_dotenv()

class QuizSession:
    BASE_TIME_PER_DIFFICULTY = {
        "ekstra mudah": 40,
        "sangat mudah": 35,
        "mudah": 30,
        "sedang": 25,
        "sulit": 20,
        "sangat sulit": 20,
        "legendaris": 20,
        "mytic": 20
    }
    MIN_TIMER_SECONDS = 8  # batas minimal timer

    def __init__(self, exp_module, question_manager):
        self.exp_module = exp_module
        self.question_manager = question_manager
        self.current_question = None
        self.current_level = 1
        self.current_exp = 0
        self.current_streak = 0
        self.wrong_streak = 0  # Tambahan: tracking salah berturut-turut
        self.last_result = None
        self.waiting_for_start = True  # Quiz belum dimulai

    def get_timer_seconds(self, difficulty, level):
        base_time = self.BASE_TIME_PER_DIFFICULTY.get(difficulty, 25)
        timer = base_time - (level // 2)
        return max(timer, self.MIN_TIMER_SECONDS)

    def _get_next_question(self):
        self.current_question = self.question_manager.get_random_question(self.current_level)
        self.last_result = None
        difficulty = self.current_question.get('difficulty', 'sedang')
        timer_seconds = self.get_timer_seconds(difficulty, self.current_level)
        self.current_question['timer_seconds'] = timer_seconds
        self.current_question['show_timer'] = True  # Timer ditampilkan saat soal aktif
        return self.current_question

    def get_next_question(self):
        # Alias untuk kompatibilitas kode lama
        return self._get_next_question()

    def start_quiz(self):
        # Dipanggil saat tombol mulai ditekan
        self.waiting_for_start = False
        question = self._get_next_question()
        return question

    def next_question(self):
        # Dipanggil saat tombol soal berikutnya ditekan
        question = self._get_next_question()
        return question

    def _normalize_answer(self, ans):
        # Normalisasi: lowercase, strip, hapus trailing titik/koma/spasi
        if not isinstance(ans, str):
            ans = str(ans)
        return ans.strip().lower().rstrip("., ")

    def answer_question(self, user_answer):
        correct_answer = self.current_question['answer']
        difficulty = self.current_question.get('difficulty', 'sedang')
        is_correct = (self._normalize_answer(user_answer) == self._normalize_answer(correct_answer))

        level_before = self.current_level

        if is_correct:
            self.current_streak += 1
            self.wrong_streak = 0  # Reset wrong streak jika benar
            exp_change = self.exp_module.get_total_exp(
                difficulty=difficulty,
                streak=(self.current_streak >= 3)
            )
            explanation = "Jawaban Anda benar!"
        else:
            self.current_streak = self.exp_module.reset_streak_on_wrong(self.current_streak)
            self.wrong_streak += 1
            exp_change = self.exp_module.get_wrong_answer_penalty(self.current_level)
            # Tambahan penalti salah berturut-turut di level tinggi
            extra_penalty = self.exp_module.get_extra_wrong_streak_penalty(self.current_level, self.wrong_streak)
            exp_change += extra_penalty
            if extra_penalty < 0:
                explanation = "⚠️ Anda salah 3x berturut-turut di level tinggi! Penalti ekstra diberikan dan streak di-reset."
                self.wrong_streak = 0  # Reset wrong streak setelah penalti ekstra
            else:
                explanation = ""

        self.current_exp += exp_change
        self.current_exp = max(self.current_exp, 0)

        new_level = self.exp_module.check_level_up(self.current_exp, self.current_level)
        self.current_level = new_level

        self.last_result = {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "exp_change": exp_change,
            "level_before": level_before,
            "level_after": self.current_level,
            "streak": self.current_streak,
            "explanation": explanation
        }
        self.current_question = None  # reset current_question agar soal baru diambil setelah submit
        return self.last_result

    def get_status(self):
        # Sertakan timer_seconds jika ada current_question
        timer_seconds = None
        show_timer = False
        if self.current_question:
            difficulty = self.current_question.get('difficulty', 'sedang')
            timer_seconds = self.get_timer_seconds(difficulty, self.current_level)
            show_timer = True
        return {
            "level": self.current_level,
            "exp": self.current_exp,
            "streak": self.current_streak,
            "current_question": self.current_question,
            "last_result": self.last_result,
            "timer_seconds": timer_seconds,
            "show_timer": show_timer,
            "waiting_for_start": self.waiting_for_start
        }
