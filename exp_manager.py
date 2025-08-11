# exp_manager.py

def get_base_exp(difficulty):
    # Update sesuai instruksi
    return {
        "ekstra mudah": 8,
        "sangat mudah": 12,
        "mudah": 15,
        "sedang": 25,
        "sulit": 40,
        "sangat sulit": 55,
        "legendaris": 80,
        "mytic": 120
    }.get(difficulty.lower(), 0)

def get_action_bonus(is_fast=False, is_open=False, streak=False, used_ai=False):
    bonus = 0
    if is_fast:
        bonus += 5
    if is_open:
        bonus += 20
    if streak:
        bonus += 10
    if used_ai:
        bonus -= 5
    return bonus

def get_total_exp(difficulty, is_fast=False, is_open=False, streak=False, used_ai=False):
    base = get_base_exp(difficulty)
    bonus = get_action_bonus(is_fast, is_open, streak, used_ai)
    return max(base + bonus, 0)  # EXP tidak boleh negatif

def get_wrong_answer_penalty(level):
    # Update sesuai instruksi
    if level <= 5:
        return 0
    elif level <= 10:
        return -5
    elif level <= 20:
        return -10
    elif level <= 40:
        return -20
    elif level <= 60:
        return -30
    elif level <= 80:
        return -50
    elif level <= 100:
        return -80
    else:
        return -80

def get_extra_wrong_streak_penalty(level, wrong_streak):
    # Penalti tambahan jika salah 3x berturut-turut di level 50+
    if level >= 50 and wrong_streak >= 3:
        return -100
    return 0

def reset_streak_on_wrong(streak):
    # Reset streak jika salah
    return 0

# Total EXP dibutuhkan untuk naik level
LEVEL_THRESHOLDS = {}
max_level = 100
exp = 0
LEVEL_THRESHOLDS[1] = exp
for lvl in range(2, max_level + 1):
    # Rumus: threshold naik makin tinggi setiap level
    exp += 50 + (lvl * 20)
    LEVEL_THRESHOLDS[lvl] = exp

def check_level_up(current_exp, current_level):
    next_level = current_level
    while (next_level + 1 in LEVEL_THRESHOLDS and 
           current_exp >= LEVEL_THRESHOLDS[next_level + 1]):
        next_level += 1
    return next_level

def get_timer_seconds(difficulty, level):
    # Waktu dasar per difficulty
    base_times = {
        "ekstra mudah": 40,
        "sangat mudah": 35,
        "mudah": 30,
        "sedang": 25,
        "sulit": 20,
        "sangat sulit": 20,
        "legendaris": 20,
        "mytic": 20
    }
    waktu_dasar = base_times.get(difficulty.lower(), 20)
    waktu_timer = max(waktu_dasar - (level // 2), 8)
    return waktu_timer
