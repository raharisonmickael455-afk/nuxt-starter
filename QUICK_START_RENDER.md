# 📋 CHECKLIST - Déploiement Render Express

## ✅ Fichiers Created

Tous les fichiers nécessaires ont été générés :

```
✓ requirements.txt          → Dépendances (avec gunicorn)
✓ Procfile                  → Configuration démarrage
✓ gunicorn_config.py        → Configuration Gunicorn
✓ .env.example              → Variables d'environnement
✓ .gitignore                → Fichiers à ignorer
✓ app.py (modifié)          → Supporte variable PORT
✓ RENDER_DEPLOYMENT.md      → Guide complet
```

## 🚀 Steps Rapides pour Render

### 1. Préparer GitHub
```bash
git add .
git commit -m "Préparation Render: gunicorn + config PORT"
git push origin main
```

### 2. Sur Render Dashboard

1. **New** → **Web Service**
2. Connecter GitHub → Sélectionner le repo
3. Remplir:
   - **Name:** `facebook-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --config gunicorn_config.py app:app`

4. **Advanced** → Ajouter Environment Variables:
   ```
   PORT = 10000
   FLASK_ENV = production
   SECRET_KEY = votre-clé-très-longue
   ```

5. **Create Web Service** ✅

### 3. Vérifier

- Attendre 3-5 min pour le build
- Cliquer sur l'URL fournie
- Vous devez voir le JSON de bienvenue

## 📝 Modifications Clés

| Fichier | Changement |
|---------|-----------|
| **app.py** | Port dynamique via `os.environ.get('PORT')` |
| **requirements.txt** | Ajout gunicorn==21.2.0 |
| **Nouveau: Procfile** | Commande démarrage pour Render |
| **Nouveau: gunicorn_config.py** | Config serveur production |

## ⚠️ Points Importants

- **Port**: Render l'attribue automatiquement (10000+)
- **Debug**: Activé seulement si `FLASK_ENV=development`
- **DB**: SQLite persiste mais Render redémarre les services (préférer PostgreSQL)
- **Secret Key**: À CHANGER avant production !

## 🔐 Sécurité

Avant production, sur Render Dashboard:

1. Aller dans votre service
2. **Environment** → Éditer
3. Changer `SECRET_KEY` par une valeur sécurisée unique

## 📚 Documentation Complète

Voir **RENDER_DEPLOYMENT.md** pour :
- Troubleshooting détaillé
- Configuration PostgreSQL
- Monitoring et logs
- Mise à jour automatique (auto-deploy)

---

**Besoin d'aide ?** Consultez les logs du service sur Render ! 🚀
