import os
from flask import Flask, request, jsonify, send_from_directory
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
    or open("secret.txt").read().strip()
)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    well = data.get("well", "")
    fix = data.get("fix", "")
    review = data.get("review", "")
    notes = data.get("notes", "")
    if well or fix or review:
        notes = (
            "Went well: " + well + "\n"
            "One fix: " + fix + "\n"
            "Review next: " + review
        )

    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=280,
        messages=[{
            "role": "user",
            "content":
                "Write a debrief draft. Instructor edits before anyone else sees it.\n"
                "Write as the instructor. You or short commands. Never I.\n"
                "Sound like a tired human instructor, not ChatGPT.\n"
                "Short. Fragments ok. Like: dont read off the board.\n"
                "Use ONLY what the instructor typed. Do not invent drills, chair flying, checklists, or extra facts.\n"
                "If they only wrote one word, stay with that word. Do not pad.\n"
                "If a section is empty or nonsense, write: Not provided.\n"
                "Australian flight training. Simple words a student understands.\n"
                "No # and no markdown. Exactly three short parts:\n"
                "Went well: ...\n"
                "One fix: ...\n"
                "Review next: ...\n"
                "Instructor notes:\n" + notes
        }],
    )
    return jsonify({"text": r.content[0].text})

if __name__ == "__main__":
    app.run(port=5000)