import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "mathieulelievre8@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def contact():
    data = request.get_json(silent=True) or request.form
    nom = data.get('name')
    email_visiteur = data.get('email')
    message_visiteur = data.get('message')

    if not SENDER_PASSWORD:
        return jsonify({"status": "error", "message": "SENDER_PASSWORD not configured"}), 500

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    msg['Subject'] = f"Nouveau message Portfolio de : {nom}"

    corps_message = f"""
    Nouveau contact depuis le site !

    Nom : {nom}
    Email : {email_visiteur}

    Message :
    {message_visiteur}
    """
    msg.attach(MIMEText(corps_message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return jsonify({"status": "success", "message": "Email envoyé !"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
