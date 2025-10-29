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
    # If frontend provided a brain, prefer it; otherwise try to load knowledge.json
    brain = data.get("brain")
    if not brain:
        try:
            import json
            with open(os.path.join('knowledge', 'knowledge.json'), 'r', encoding='utf-8') as f:
                brain = json.load(f)
        except Exception:
            brain = None

    # Simple local response that uses the brain if available
    if brain:
        tone = brain.get('personality', {}).get('tone', '')
        ag_first = None
        ag = brain.get('agriculture')
        if isinstance(ag, dict):
            # pick a short agriculture fact to include
            for k, v in ag.items():
                if isinstance(v, dict):
                    if 'overview' in v:
                        ag_first = v.get('overview')
                        break
                    if 'description' in v:
                        ag_first = v.get('description')
                        break
        reply = f"🤖 CriderGPT (Offline) [{tone}]: {prompt}"
        if ag_first:
            reply += f"\n\nLocal knowledge (agriculture): {ag_first}"
    else:
        reply = f"🤖 CriderGPT (Offline): '{prompt}' processed locally."
    return jsonify({"response": reply})


if __name__ == "__main__":
    # Run the Flask dev server on 127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
