# exp_manager.py

def get_base_exp(difficulty):
    return {
        "mudah": 15,
        "sedang": 25,
        "sulit": 40
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
    if level <= 5:
        return 0
    elif level <= 10:
        return -5
    elif level <= 15:
        return -10
    elif level <= 20:
        return -15
    else:
        return -20

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
