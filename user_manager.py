import json
import os
import hashlib

USER_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username sudah terdaftar."
    users[username] = {
        "password": hash_password(password),
        "level": 1,
        "exp": 0,
        "streak": 0
    }
    save_users(users)
    return True, "Registrasi berhasil."

def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Username tidak ditemukan."
    if users[username]["password"] != hash_password(password):
        return False, "Password salah."
    return True, "Login berhasil."

def get_user_progress(username):
    users = load_users()
    return users.get(username, {})

def update_user_progress(username, level, exp, streak):
    users = load_users()
    if username in users:
        users[username]["level"] = level
        users[username]["exp"] = exp
        users[username]["streak"] = streak
        save_users(users)
