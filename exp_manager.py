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
LEVEL_THRESHOLDS = {
    1: 0, 2: 50, 3: 120, 4: 210, 5: 320,
    6: 450, 7: 600, 8: 770, 9: 960, 10: 1170,
    11: 1400, 12: 1650, 13: 1920, 14: 2210, 15: 2520,
    16: 2850, 17: 3200, 18: 3570, 19: 3960, 20: 4370,
    21: 4800, 22: 5250, 23: 5720, 24: 6210, 25: 6720
}

def check_level_up(current_exp, current_level):
    next_level = current_level
    while (next_level + 1 in LEVEL_THRESHOLDS and 
           current_exp >= LEVEL_THRESHOLDS[next_level + 1]):
        next_level += 1
    return next_level
