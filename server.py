import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Autorise les requêtes Cross-Origin (nécessaire si le front et le back sont sur des domaines différents)

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mathieulelivere8@gmail.com"

# Sécurité : Récupération du mot de passe via les variables d'environnement du serveur
# Cela évite de hardcoder des credentials sensibles dans le code source
SENDER_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')

@app.route('/contact', methods=['POST'])
def contact():
    # Extraction des données du formulaire
    data = request.form
    nom = data.get('name')
    email_visiteur = data.get('email')
    message_visiteur = data.get('message')

    print(f"Log: Tentative d'envoi d'email de la part de {nom}")

    # Construction du message MIME
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    msg['Subject'] = f"Portfolio Contact : {nom}"

    corps_message = f"Nom: {nom}\nEmail: {email_visiteur}\nMessage:\n{message_visiteur}"
    msg.attach(MIMEText(corps_message, 'plain'))

    try:
        if not SENDER_PASSWORD:
            raise ValueError("Variable d'environnement 'MY_EMAIL_PASSWORD' manquante.")

        # Connexion sécurisée au serveur Gmail
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return jsonify({"status": "success", "message": "Email envoyé avec succès."})
        
    except Exception as e:
        print(f"Erreur SMTP : {e}")
        return jsonify({"status": "error", "message": "Erreur interne du serveur."}), 500

if __name__ == '__main__':
    # Le port 5000 est le standard Flask pour le développement local
    app.run(debug=True, port=5000)