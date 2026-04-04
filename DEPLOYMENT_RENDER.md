# Guide de Déploiement sur Render.com

## 📋 Structure du Projet

```
/mon-site
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── Procfile              # Configuration Render
├── runtime.txt           # Version Python
├── .env.example          # Variables d'environnement exemple
├── templates/
│   └── index.html        # Page HTML principale
└── static/
    ├── styles.css        # Feuilles de style
    ├── script.js         # JavaScript
    ├── manifest.json     # PWA manifest
    ├── sw.js             # Service Worker
    ├── robots.txt        # SEO
    └── sitemap.xml       # Sitemap
```

## 🚀 Instructions de Déploiement

### 1. Prérequis
- Compte [Render.com](https://render.com) (gratuit)
- Git installé localement
- Repository GitHub

### 2. Créer un Repository GitHub

```bash
git init
git add .
git commit -m "Initial commit - Prepare for Render deployment"
git remote add origin https://github.com/votreusername/votre-repo.git
git push -u origin main
```

### 3. Déployer sur Render

1. **Aller sur Render.com** et se connecter
2. **Cliquer sur "New +"** → **"Web Service"**
3. **Sélectionner votre repository GitHub**
4. **Remplir les détails:**
   - Name: `facebook-login-app` (ou votre nom)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: `Free` ou `Starter`

### 4. Configurer les Variables d'Environnement

1. Aller dans **Settings** de votre service
2. Ajouter sous **Environment Variables**:

```
SECRET_KEY=une-clé-très-longue-et-aléatoire
DEBUG=False
PORT=5000
```

Pour générer une clé sécurisée (Python):
```python
import secrets
print(secrets.token_hex(32))
```

### 5. Variables d'Environnement sur Render

| Variable | Valeur | Description |
|----------|--------|-------------|
| `SECRET_KEY` | `<clé aléatoire longue>` | Clé de sécurité Flask |
| `DEBUG` | `False` | Mode développement désactivé |
| `PORT` | `5000` | Port (Render l'assigne automatiquement) |

### 6. Fichiers Essentiels

#### ✅ `Procfile`
```
web: gunicorn app:app
```

#### ✅ `runtime.txt`
```
python-3.11.7
```

#### ✅ `requirements.txt`
```
Flask==2.3.2
Flask-CORS==4.0.0
Werkzeug==2.3.6
gunicorn==21.2.0
python-dotenv==1.0.0
```

#### ✅ `.env.example`
```
PORT=5000
DEBUG=False
SECRET_KEY=votre-clé-secrète
```

### 7. Test Local Avant Déploiement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Créer un fichier .env
copy .env.example .env

# Lancer l'app localement
python app.py
```

L'app sera disponible sur: `http://localhost:5000`

### 8. Vérifier le Déploiement

Une fois déployé sur Render:
- URL: `https://votre-app.onrender.com`
- Logs: Dashboard Render → Logs
- Health: S'affiche automatiquement sur le dashboard

### 9. Troubleshooting

#### App ne démarre pas
```bash
# Vérifier les logs (Render Dashboard)
# S'assurer que gunicorn est dans requirements.txt
# S'assurer que Procfile existe et est correct
```

#### Static files ne se chargent pas
```
# Vérifier que les dossiers templates/ et static/ existent
# Vérifier que app.py utilise render_template()
# Vérifier les url_for() dans les templates
```

#### Base de données vide après redéploiement
```
# Render ne persiste pas les fichiers locaux
# Utiliser une vraie base de données:
# - PostgreSQL (gratuit sur Render)
# - MongoDB Atlas
```

### 10. Optimisations Production

- [ ] Utiliser une base de données externe (sqlite3 = non-persistant)
- [ ] Mettre `DEBUG=False`
- [ ] Générer une clé `SECRET_KEY` sécurisée
- [ ] Utiliser HTTPS (Render le fait automatiquement)
- [ ] Ajouter une validation des données robuste
- [ ] Implémenter le logging approprié

### 11. Domaine Personnalisé

1. Aller dans **Settings** → **Custom Domain**
2. Suivre les instructions pour pointer votre DNS
3. Certificat SSL/TLS gratuit automatique

## 📞 Support

- [Render Docs](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Gunicorn](https://gunicorn.org)

## ⚠️ Notes Importantes

- **Fichier de log** (`credentials_log.txt`): Cet application capture les données - à utiliser uniquement à des fins de test légales
- **Données sensibles**: Ne jamais commiter `.env` avec les vraies clés
- **SSL**: Render fourni SSL gratuit

---

**Prêt à déployer? Bonne chance! 🚀**
