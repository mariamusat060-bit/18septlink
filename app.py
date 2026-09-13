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
    notes = request.json.get("notes", "")
    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content":
            "Write a debrief draft. Instructor will edit before anyone else sees it.\n"
            "Write as the instructor. Use you or short commands. Never I.\n"
            "Tone: short coaching bullets like 'dont read off the board'.\n"
            "Use ONLY the instructor notes. Do not invent maneuvers, checklists, or facts.\n"
            "If a section is empty or nonsense, write: Not provided.\n"
            "Australian training. Clear simple words.\n"
            "No # and no markdown. Exactly three short parts:\n"
            "Went well: ...\n"
            "One fix: ...\n"
            "Review next: ...\n"
            "Notes:\n" + notes
        }],
    )
    return jsonify({"text": r.content[0].text})

if __name__ == "__main__":
    app.run(port=5000)