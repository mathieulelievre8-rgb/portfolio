import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client # Importation de Supabase

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- CONFIGURATION SUPABASE ---
# On récupère les clés depuis les variables d'environnement (comme pour l'email)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# On initialise la connexion
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- ROUTE GET : Lire la base de données ---
@app.route('/api/messages', methods=['GET'])
def get_messages():
    # On demande à Supabase : "Donne-moi tout, trié par date décroissante"
    response = supabase.table('messages').select("*").order('created_at', desc=True).execute()
    
    # Supabase renvoie les données dans response.data
    # Note : On adapte un peu le format pour que ton frontend comprenne (on mappe 'uid' vers 'id')
    formatted_messages = []
    for msg in response.data:
        formatted_messages.append({
            "id": msg['uid'], # Le front utilise 'id' pour supprimer, nous on a stocké ça dans 'uid'
            "auteur": msg['auteur'],
            "texte": msg['texte']
        })
        
    return jsonify(formatted_messages)

# --- ROUTE POST : Écrire dans la base ---
@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.json
    auteur = data.get('auteur')
    texte = data.get('texte')

    if not auteur or not texte:
        return jsonify({"error": "Données manquantes"}), 400

    # On crée l'objet à envoyer à Supabase
    nouveau_message = {
        "uid": str(uuid.uuid4()), # On génère l'ID unique ici
        "auteur": auteur, 
        "texte": texte
    }
    
    # On insère dans la table 'messages'
    try:
        supabase.table('messages').insert(nouveau_message).execute()
        return jsonify({"success": True, "message": "Sauvegardé en base !"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ROUTE DELETE : Supprimer de la base ---
@app.route('/api/messages/<msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    try:
        # On dit à Supabase : Supprime la ligne où la colonne 'uid' est égale à msg_id
        supabase.table('messages').delete().eq('uid', msg_id).execute()
        return jsonify({"success": True, "message": "Supprimé de la base !"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)