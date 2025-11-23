import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Autorise tout le monde (CORS)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- MÉMOIRE TEMPORAIRE ---
messages = [
    {"id": "1", "auteur": "System", "texte": "Initialisation du protocole de discussion... 🟢"},
    {"id": "2", "auteur": "Admin", "texte": "Bienvenue sur le terminal."}
]

# --- ROUTES API ---
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.json
    auteur = data.get('auteur')
    texte = data.get('texte')

    if not auteur or not texte:
        return jsonify({"error": "Données manquantes"}), 400

    nouveau_message = {
        "id": str(uuid.uuid4()), 
        "auteur": auteur, 
        "texte": texte
    }
    messages.append(nouveau_message)
    return jsonify({"success": True, "message": "Donnée injectée !"})

@app.route('/api/messages/<msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    global messages
    messages = [msg for msg in messages if msg['id'] != msg_id]
    return jsonify({"success": True, "message": "Donnée purgée !"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)