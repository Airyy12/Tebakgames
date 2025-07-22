import json
import random

class QuestionManager:
    def __init__(self, filepath: str = "questions.json"):
        """Muat semua soal dari file JSON dan indeks per level"""
        with open(filepath, "r", encoding="utf-8") as f:
            self.questions = json.load(f)
        
        self.level_index = {}
        for q in self.questions:
            level = q["level"]
            if level not in self.level_index:
                self.level_index[level] = []
            self.level_index[level].append(q)

    def get_random_question(self, level: int) -> dict:
        """Ambil satu soal acak dari level tertentu"""
        if level in self.level_index:
            return random.choice(self.level_index[level])
        else:
            raise ValueError(f"Tidak ada soal untuk level {level}.")

    def get_questions_by_level(self, level: int, count: int = 5) -> list:
        """Ambil beberapa soal acak dari level tertentu"""
        if level in self.level_index:
            return random.sample(self.level_index[level], min(count, len(self.level_index[level])))
        else:
            raise ValueError(f"Tidak ada soal untuk level {level}.")

    def get_question_by_id(self, qid: int) -> dict:
        """Cari soal berdasarkan ID"""
        for q in self.questions:
            if q["id"] == qid:
                return q
        raise ValueError(f"Soal dengan ID {qid} tidak ditemukan.")
