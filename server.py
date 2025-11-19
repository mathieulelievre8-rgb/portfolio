import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app) # Sécurité

# --- CONFIGURATION DE TON EMAIL (A REMPLIR) ---
# C'est l'adresse qui va ENVOYER le mail (le robot)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mathieulelievre8@gmail.com" 
load_dotenv()
# On lit le mot de passe depuis la variable d'environnement `SENDER_PASSWORD`.
# Ne laisse jamais de secret en dur dans le dépôt.
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

if not SENDER_PASSWORD:
    print("Warning: SENDER_PASSWORD not set. Define it in your environment or in a local .env file")

@app.route('/contact', methods=['POST'])
def contact():
    # 1. Récupération des données
    data = request.form
    nom = data.get('name')
    email_visiteur = data.get('email') # L'email de la personne qui te contacte
    message_visiteur = data.get('message')

    print(f"Tentative d'envoi d'email de la part de {nom}...")

    # 2. Préparation de l'email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL # Tu te l'envoies à toi-même
    msg['Subject'] = f"Nouveau message Portfolio de : {nom}"

    # Le corps du mail
    corps_message = f"""
    Nouveau contact depuis le site !
    
    Nom : {nom}
    Email : {email_visiteur}
    
    Message :
    {message_visiteur}
    """
    msg.attach(MIMEText(corps_message, 'plain'))

    # 3. Connexion au serveur Gmail et Envoi
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() # On sécurise la connexion
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("✅ Email envoyé avec succès !")
        return jsonify({"status": "success", "message": "Email envoyé !"})
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)