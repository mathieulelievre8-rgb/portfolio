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