from badge_manager import check_and_give_badges

def process_answer(user, answer):
    # ...existing code...
    # Update jumlah soal dijawab
    user['answered_count'] = user.get('answered_count', 0) + 1
    # Cek dan berikan badge
    check_and_give_badges(user)
    # ...existing code...

def level_up(user):
    # ...existing code...
    # Cek dan berikan badge setelah naik level
    check_and_give_badges(user)
    # ...existing code...
