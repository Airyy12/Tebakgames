import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    # Format: {username: {level, exp, streak, ...}}
    users = []
    for username, info in data.items():
        users.append({
            "username": username,
            "level": info.get("level", 1),
            "exp": info.get("exp", 0),
            "streak": info.get("streak", 0)
        })
    return users

def get_leaderboard(sort_by="level", top_n=20):
    users = load_users()
    if sort_by not in ["level", "exp", "streak"]:
        sort_by = "level"
    users_sorted = sorted(users, key=lambda x: x[sort_by], reverse=True)
    return users_sorted[:top_n]
