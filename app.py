import os
import psycopg2
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/", methods=["GET"])
def home():
    return "Bot aktif 🚀"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    try:
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (chat_id, message) VALUES (%s, %s)",
                (chat_id, text)
            )
            conn.commit()
            cur.close()
            conn.close()

            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"Masuk: {text}"
                }
            )

    except Exception as e:
        print("ERROR:", e)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)