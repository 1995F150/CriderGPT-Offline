from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder="offline_ui/dist")

@app.route("/")
def serve_index():
    # serve the built frontend index
    return send_from_directory("offline_ui/dist", "index.html")


@app.route("/api/respond", methods=["POST"])
def respond():
    data = request.get_json()
    prompt = data.get("prompt", "")
    reply = f"🤖 CriderGPT (Offline): '{prompt}' processed locally."
    return jsonify({"response": reply})


if __name__ == "__main__":
    # Run the Flask dev server on 127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
