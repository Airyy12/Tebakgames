BADGE_LIST = [
    {"id": "streak_master", "name": "Streak Master", "desc": "Mencapai streak 10 jawaban benar berturut-turut.", "icon": "🔥"},
    {"id": "streak_legend", "name": "Streak Legend", "desc": "Mencapai streak 25 jawaban benar berturut-turut.", "icon": "🔥"},
    {"id": "level_5", "name": "Level Up 5", "desc": "Naik ke level 5.", "icon": "🏅"},
    {"id": "level_10", "name": "Level Up 10", "desc": "Naik ke level 10.", "icon": "🏅"},
    {"id": "level_20", "name": "Level Up 20", "desc": "Naik ke level 20.", "icon": "🏅"},
    {"id": "quiz_warrior", "name": "Quiz Warrior", "desc": "Menjawab 100 soal.", "icon": "⚔️"},
    {"id": "quiz_hero", "name": "Quiz Hero", "desc": "Menjawab 500 soal.", "icon": "🦸"},
    {"id": "quiz_legend", "name": "Quiz Legend", "desc": "Menjawab 1000 soal.", "icon": "🏆"},
    {"id": "first_login", "name": "First Login", "desc": "Login pertama kali ke aplikasi.", "icon": "👋"},
    {"id": "first_win", "name": "First Win", "desc": "Menjawab soal pertama dengan benar.", "icon": "✅"},
    {"id": "perfect_session", "name": "Perfect Session", "desc": "Menjawab semua soal dalam satu sesi dengan benar.", "icon": "🌟"},
    {"id": "early_bird", "name": "Early Bird", "desc": "Menjawab soal dalam waktu kurang dari 10 detik.", "icon": "⏱️"},
    {"id": "speedster", "name": "Speedster", "desc": "Menjawab 10 soal berturut-turut masing-masing dalam waktu <10 detik.", "icon": "⚡"},
    {"id": "comeback_kid", "name": "Comeback Kid", "desc": "Pernah salah 3 kali berturut-turut, lalu berhasil streak 5 jawaban benar.", "icon": "🔄"},
    {"id": "persistent_player", "name": "Persistent Player", "desc": "Login selama 7 hari berturut-turut.", "icon": "📅"},
    {"id": "night_owl", "name": "Night Owl", "desc": "Menjawab soal antara jam 00:00 - 05:00.", "icon": "🌙"},
    {"id": "explorer", "name": "Explorer", "desc": "Menjawab soal dari 5 kategori/topik berbeda.", "icon": "🧭"},
    {"id": "lucky_guess", "name": "Lucky Guess", "desc": "Menjawab benar soal dengan tingkat kesulitan tertinggi.", "icon": "🍀"},
    {"id": "socializer", "name": "Socializer", "desc": "Mengajak teman untuk bergabung dan bermain quiz.", "icon": "🤝"},
    {"id": "feedback_giver", "name": "Feedback Giver", "desc": "Mengirimkan saran/feedback melalui aplikasi.", "icon": "💬"},
]

def get_badge_info(badge_id):
    for badge in BADGE_LIST:
        if badge["id"] == badge_id:
            return badge
    return None

def check_and_award_badges(user, event):
    # event: dict berisi info aksi user (misal: streak, level, soal dijawab, waktu, dsb)
    awarded = []
    # Contoh logika sederhana (implementasi detail di quiz_session.py atau app.py)
    if event.get("streak", 0) >= 10:
        awarded.append("streak_master")
    if event.get("streak", 0) >= 25:
        awarded.append("streak_legend")
    if event.get("level", 0) >= 5:
        awarded.append("level_5")
    if event.get("level", 0) >= 10:
        awarded.append("level_10")
    if event.get("level", 0) >= 20:
        awarded.append("level_20")
    if event.get("total_answered", 0) >= 100:
        awarded.append("quiz_warrior")
    if event.get("total_answered", 0) >= 500:
        awarded.append("quiz_hero")
    if event.get("total_answered", 0) >= 1000:
        awarded.append("quiz_legend")
    # ...tambahkan logika badge lain sesuai milestone...
    return awarded

def check_and_give_badges(user_data):
    # Cek dan berikan badge sesuai progress user
    # Contoh:
    if user_data.get("answered_count", 0) >= 100:
        user_data.setdefault("badges", []).append("Quiz Warrior")
    # ...tambahkan logika badge lain...
