import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# SendGrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "mathieulelievre8@gmail.com")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def contact():
    data = request.get_json(silent=True) or request.form
    nom = data.get('name')
    email_visiteur = data.get('email')
    message_visiteur = data.get('message')

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
            return jsonify({"status": "success", "message": "Email envoyé !"})
        else:
            return jsonify({"status": "error", "message": f"SendGrid error {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
