# 🚀 Guide de Déploiement sur Render

Ce guide vous explique comment déployer votre application Flask sur la plateforme **Render**.

## 📋 Prérequis

1. Un compte GitHub (avec votre code pushé)
2. Un compte [Render](https://render.com) (gratuit)
3. Git installé sur votre machine

## 🔧 Préparation Locale

### 1. Vérifier les fichiers requis

Assurez-vous que tous ces fichiers sont présents à la racine de votre projet :

```
✓ app.py
✓ requirements.txt
✓ Procfile
✓ gunicorn_config.py
✓ .gitignore
```

### 2. Créer/Mettre à jour .gitignore

Créez un fichier `.gitignore` à la racine :

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Database
facebook.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
```

### 3. Vérifier requirements.txt

Assurez-vous que `requirements.txt` contient toutes les dépendances :

```
Flask==3.0.0
Flask-CORS==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

### 4. Push le code sur GitHub

```bash
git add .
git commit -m "Préparation pour déploiement sur Render"
git push origin main
```

## 🌐 Déploiement sur Render

### Étape 1 : Créer un nouveau Web Service

1. Allez sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquez sur **"New +"** → **"Web Service"**
3. Sélectionnez **"Deploy from GitHub"**
4. Connectez votre compte GitHub si nécessaire
5. Sélectionnez votre repository

### Étape 2 : Configurer le Service

Remplissez les informations suivantes :

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `facebook-backend` (ou votre nom) |
| **Environment** | `Python 3` |
| **Region** | Choisir la plus proche de vous |
| **Branch** | `main` (ou votre branche) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --config gunicorn_config.py app:app` |

### Étape 3 : Ajouter des Variables d'Environnement

Cliquez sur **"Advanced"** et ajoutez les variables d'environnement :

```
PORT = 10000
FLASK_ENV = production
```

**Note :** Render attribue automatiquement le PORT. La configuration gunicorn le capture.

### Étape 4 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Rendez-vous attend 3-5 minutes pour le déploiement initial
3. Une fois terminé, vous verrez votre URL de service (ex: `https://facebook-backend.onrender.com`)

## ✅ Vérifier le Déploiement

### Test rapide

```bash
# Testez votre endpoint
curl https://votre-app.onrender.com/

# Vous devez recevoir:
# {
#   "message": "Serveur Facebook Login Backend",
#   "version": "1.0",
#   "status": "En cours d'exécution",
#   ...
# }
```

### Logs en Direct

Pour voir les logs en temps réel :

1. Allez sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquez sur votre service
3. Onglet **"Logs"**

## 🔄 Mises à Jour Futures

Après chaque push sur GitHub :

1. Render détecte automatiquement les changements
2. Un nouveau déploiement commence (auto-deploy est activé par défaut)
3. Les logs vous montrent la progression

### Pour désactiver l'auto-deploy :

Aller dans **Settings** → **Auto-Deploy** → Changer selon vos préférences

## ⚠️ Problèmes Courants

### 1. **Erreur 502 Bad Gateway**

- Vérifiez les logs pour les erreurs
- Assurez-vous que `Procfile` contient la bonne commande
- Vérifiez que `port=5000` n'est plus hardcodé dans app.py

### 2. **ModuleNotFoundError**

- Vérifiez que `requirements.txt` est à la racine
- Vérifiez que toutes les dépendances y sont listées
- Reconstruisez le service : **Settings** → **Redeploy**

### 3. **Base de données disparaît après redémarrage**

Render redémarre les services. SQLite n'est pas idéal pour Render.

**Solution recommandée :** Utiliser PostgreSQL (gratuit sur Render)
- Voir guide PostgreSQL (optionnel)

### 4. **Timeout (H12 error)**

Augmentez le timeout. Éditez `gunicorn_config.py` :

```python
timeout = 60  # au lieu de 30
```

Puis redéployez.

## 📊 Surveillance et Maintenance

### Health Checks

Render fait automatiquement des health checks. Assurez-vous que votre endpoint `/` répond rapidement.

### Métriques

Dans le **Dashboard** → **Metrics**, vous pouvez voir :
- CPU usage
- Memory usage
- Network I/O
- Restarts

## 🔐 Sécurité

### IMPORTANT : Avant la production

1. **Changez la clé secrète** dans app.py :
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-this')
   ```

2. Ajoutez la variable d'environnement sur Render :
   - Dashboard → Your Service → Environment
   - Ajoutez : `SECRET_KEY = votre-clé-sécurisée-très-longue`

3. Mettez `debug=False` (configuré automatiquement en production)

## 📝 Fichiers de Configuration Expliqués

### **Procfile**
Indique à Render comment démarrer votre application avec Gunicorn.

### **gunicorn_config.py**
Configuration du serveur WSGI :
- Nombre de workers
- Timeouts
- Logging
- Port dynamique via variable d'environnement

### **requirements.txt**
Toutes les dépendances Python nécessaires.

## 🎯 Checklist Final Déploiement

- [ ] Code pushé sur GitHub
- [ ] `.gitignore` créé
- [ ] `requirements.txt` à jour
- [ ] `Procfile` présent
- [ ] `gunicorn_config.py` présent
- [ ] `app.py` utilise `os.environ.get('PORT')`
- [ ] Service créé sur Render
- [ ] Variables d'environnement configurées
- [ ] Déploiement réussi (pas d'erreur 502)
- [ ] Endpoint `/` répond correctement
- [ ] Logs visibles sans erreur

## 📚 Ressources Utiles

- [Documentation Render](https://render.com/docs)
- [Déployer Flask sur Render](https://render.com/docs/deploy-flask)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)

---

**Besoin d'aide ?** Consultez les logs sur le Dashboard Render pour plus de détails ! 🚀
