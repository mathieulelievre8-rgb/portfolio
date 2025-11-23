import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- CHANGEMENT ICI : PORT 465 ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # On passe sur le port sécurisé SSL direct
SENDER_EMAIL = "mathieulelievre8@gmail.com" # <--- VÉRIFIE QUE C'EST BIEN TON EMAIL ICI
SENDER_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')

@app.route('/contact', methods=['POST'])
def contact():
    data = request.form
    nom = data.get('name')
    email_visiteur = data.get('email')
    message_visiteur = data.get('message')

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    msg['Subject'] = f"Portfolio Contact : {nom}"

    corps_message = f"Nom: {nom}\nEmail: {email_visiteur}\nMessage:\n{message_visiteur}"
    msg.attach(MIMEText(corps_message, 'plain'))

    try:
        if not SENDER_PASSWORD:
            return jsonify({"status": "error", "message": "Erreur config mot de passe"}), 500

        # --- CHANGEMENT ICI : SMTP_SSL et suppression de starttls ---
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        # server.starttls()  <-- ON A SUPPRIMÉ CETTE LIGNE, ELLE CASSE TOUT EN SSL
        
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return jsonify({"status": "success", "message": "Email envoyé avec succès."})
        
    except Exception as e:
        print(f"Erreur SMTP : {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)