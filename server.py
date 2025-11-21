import os # Importation de la librairie os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS # On s'assure que c'est importé

app = Flask(__name__)
# FIX CRUCIAL : Autorise TOUTES les connexions externes (CORS)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Configuration SMTP (Identique)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ton.adresse.perso@gmail.com" 
SENDER_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    nom = data.get('name')
    email_visiteur = data.get('email')
    message_visiteur = data.get('message')

    # Gestion du mail (Identique)
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    msg['Subject'] = f"Portfolio Contact : {nom}"
    corps_message = f"Nom: {nom}\nEmail: {email_visiteur}\nMessage:\n{message_visiteur}"
    msg.attach(MIMEText(corps_message, 'plain'))

    try:
        if not SENDER_PASSWORD:
            return jsonify({"status": "error", "message": "Erreur interne: Mot de passe serveur non configuré."}), 500

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return jsonify({"status": "success", "message": "Email envoyé avec succès."})
        
    except Exception as e:
        print(f"Erreur SMTP : {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Cette ligne est pour le test LOCAL uniquement. 
    # Render utilise Gunicorn et l'ignore, mais on la garde pour tester sur ton PC.
    app.run(debug=True, port=5000)