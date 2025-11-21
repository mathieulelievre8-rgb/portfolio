import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# SendGrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
CORS(app) # Sécurité

# Adresse d'envoi par défaut (modifiable via env `SENDER_EMAIL`)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "mathieulelievre8@gmail.com")

load_dotenv()
# On lit la clé SendGrid depuis l'environnement
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

if not SENDGRID_API_KEY:
    print("Warning: SENDGRID_API_KEY not set. Define it in your environment or in a local .env file")

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

    # 3. Envoi via SendGrid
    if not SENDGRID_API_KEY:
        return jsonify({"status": "error", "message": "SENDGRID_API_KEY not configured"}), 500

    subject = f"Nouveau message Portfolio de : {nom}"
    corps_message = f"""
Nouveau contact depuis le site !

Nom : {nom}
Email : {email_visiteur}

Message :
{message_visiteur}
"""

    mail = Mail(
        from_email=SENDER_EMAIL,
        to_emails=SENDER_EMAIL,
        subject=subject,
        plain_text_content=corps_message,
    )

    try:
        client = SendGridAPIClient(SENDGRID_API_KEY)
        response = client.send(mail)
        if 200 <= response.status_code < 300:
            print("✅ Email envoyé avec succès via SendGrid !")
            return jsonify({"status": "success", "message": "Email envoyé !"})
        else:
            print(f"❌ SendGrid error: {response.status_code}")
            return jsonify({"status": "error", "message": f"SendGrid error {response.status_code}"}), 500
    except Exception as e:
        print(f"❌ Erreur SendGrid : {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)