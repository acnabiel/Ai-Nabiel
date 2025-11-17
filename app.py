from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "rahasia_super_aman"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset_chat():
    session.pop("chat_history", None)
    return jsonify({"message": "Percakapan telah direset."})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "Pesan kosong"}), 400

    # Ambil history
    chat_history = session.get("chat_history", [
        {"role": "system", "content": "Kamu adalah asisten AI yang ramah."}
    ])

    # Tambah pesan user
    chat_history.append({"role": "user", "content": user_message})

    try:
        # Kirim ke OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            max_tokens=300
        )

        # Ambil jawaban AI → pakai .content (BUKAN dictionary!)
        ai_reply = response.choices[0].message.content

        # Simpan ke history
        chat_history.append({
            "role": "assistant",
            "content": ai_reply
        })
        
        session["chat_history"] = chat_history

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
