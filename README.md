# Portfolio (backend)

Instructions rapides pour initialiser et déployer localement :

- Copier `.env.example` en `.env` et remplir `SENDER_PASSWORD` (ne commitez jamais `.env`).
- Installer les dépendances :

```
python -m pip install -r requirements.txt
```

- Lancer le serveur :

```
python server.py
```

Notes :
- Ce dépôt lit `SENDER_PASSWORD` depuis la variable d'environnement `SENDER_PASSWORD`.
- Pour Gmail, utilisez un mot de passe d'application si l'authentification classique est bloquée.

SendGrid (option serverless)
 - Ce dépôt prend maintenant en charge l'envoi d'emails via SendGrid pour la function serverless `api/contact.py`.
 - Définissez `SENDGRID_API_KEY` dans votre `.env` local ou dans les Environment Variables du projet Vercel.
 - Vercel installera automatiquement les dépendances listées dans `requirements.txt`.

Exemples local:
```
copy .env.example .env
# remplir .env (SENDGRID_API_KEY)
python -m pip install -r requirements.txt
python api/contact.py
```

Render deployment
- Ce projet est prêt pour déploiement sur Render en tant que Web Service.
- Étapes rapides:
	1. Créez un compte sur https://render.com et connectez votre dépôt GitHub.
	2. Créez un nouveau service "Web Service" et choisissez la branche `main`.
	3. Commande de build: laissez vide (Render installera `requirements.txt`).
	4. Start Command: `gunicorn server:app`
	5. Ajoutez les Environment Variables dans Render (Settings > Environment):
		 - `SENDGRID_API_KEY` = (votre clé SendGrid)
		 - `SENDER_EMAIL` = (optionnel)
	6. Déployez et vérifiez les logs dans Render Dashboard.

Notes:
- `Procfile` et `gunicorn` sont fournis pour faciliter le démarrage.
- Testez localement avant push: installez les dépendances et lancez `python server.py`.