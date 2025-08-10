import os
import exp_manager
from dotenv import load_dotenv

load_dotenv()

class QuizSession:
    def __init__(self, exp_module, question_manager):
        self.exp_module = exp_module
        self.question_manager = question_manager
        self.current_question = None
        self.current_level = 1
        self.current_exp = 0
        self.current_streak = 0
        self.last_result = None

    def get_next_question(self):
        self.current_question = self.question_manager.get_random_question(self.current_level)
        self.last_result = None
        return self.current_question

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
            exp_change = self.exp_module.get_total_exp(
                difficulty=difficulty,
                streak=(self.current_streak >= 3)
            )
            explanation = "Jawaban Anda benar!"
        else:
            self.current_streak = 0
            exp_change = self.exp_module.get_wrong_answer_penalty(self.current_level)
            explanation = ""  # Tidak ada penjelasan AI

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
        return {
            "level": self.current_level,
            "exp": self.current_exp,
            "streak": self.current_streak,
            "current_question": self.current_question,
            "last_result": self.last_result
        }
