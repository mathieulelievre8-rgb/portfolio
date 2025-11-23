import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# On autorise ton site GitHub à parler à ce cerveau
CORS(app, resources={r"/*": {"origins": "*"}})

# --- LA MÉMOIRE (Temporaire) ---
# Une simple liste pour stocker les messages. 
# Attention : si Render redémarre, ça s'efface (on verra les bases de données plus tard).
messages = [
    {"auteur": "Mathieu", "texte": "Bienvenue sur mon micro-forum !"},
    {"auteur": "Bot", "texte": "Le serveur est en ligne 🟢"}
]

# --- ROUTE 1 : RÉCUPÉRER LES MESSAGES (GET) ---
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

# --- ROUTE 2 : AJOUTER UN MESSAGE (POST) ---
@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.json # On reçoit du JSON cette fois
    auteur = data.get('auteur')
    texte = data.get('texte')

    if not auteur or not texte:
        return jsonify({"error": "Données incomplètes"}), 400

    # On ajoute le message à la liste
    nouveau_message = {"auteur": auteur, "texte": texte}
    messages.append(nouveau_message)
    
    return jsonify({"success": True, "message": "Ajouté !"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)