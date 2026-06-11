from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

FAQS = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi! Nice to meet you.",
    "what is ai": "AI stands for Artificial Intelligence.",
    "bye": "Goodbye! Have a great day!"
}

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_chat(message, response):
    conn = sqlite3.connect("chatbot.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_logs (user_message, bot_response, timestamp) VALUES (?, ?, ?)",
        (message, response, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Flask Chatbot Running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"response": "Please enter a message"})

    response = FAQS.get(message, "Sorry, I don't understand that question.")
    log_chat(message, response)
    return jsonify({"response": response})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
