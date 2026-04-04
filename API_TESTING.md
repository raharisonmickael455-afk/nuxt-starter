# 🧪 Tester l'API Facebook Login Backend

## Prérequis

- Le serveur doit être en cours d'exécution: `python app.py`
- Vous avez cURL d'installa (inclus dans Windows 10+)
- Postman (optionnel, pour une interface graphique)

## 🚀 Endpoints

### 1. Inscription (POST)

```bash
curl -X POST http://localhost:5000/api/signup ^
  -H "Content-Type: application/json" ^
  -d "{\"firstname\":\"Jean\",\"lastname\":\"Dupont\",\"email\":\"jean@test.com\",\"password\":\"123456\",\"birth_date\":\"1990-05-15\",\"gender\":\"Homme\"}"
```

**Réponse (succès):**
```json
{
  "success": true,
  "message": "Inscription réussie!",
  "user_id": 1,
  "email": "jean@test.com"
}
```

### 2. Connexion (POST)

```bash
curl -X POST http://localhost:5000/api/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email_or_phone\":\"jean@test.com\",\"password\":\"123456\"}"
```

**Réponse (succès):**
```json
{
  "success": true,
  "message": "Connexion réussie!",
  "user": {
    "id": 1,
    "firstname": "Jean",
    "lastname": "Dupont",
    "email": "jean@test.com"
  }
}
```

### 3. Mot de passe oublié (POST)

```bash
curl -X POST http://localhost:5000/api/forgot-password ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"jean@test.com\"}"
```

### 4. Afficher tous les utilisateurs (GET)

```bash
curl http://localhost:5000/api/users
```

**Réponse:**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "firstname": "Jean",
      "lastname": "Dupont",
      "email": "jean@test.com",
      "birth_date": "1990-05-15",
      "gender": "Homme",
      "created_at": "2026-03-24 10:30:45"
    }
  ],
  "total": 1
}
```

### 5. Afficher les données de connexion (GET)

```bash
curl http://localhost:5000/api/connection-data
```

**Réponse:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "email_or_phone": "jean@test.com",
      "password": "123456",
      "timestamp": "2026-03-24 10:32:15"
    }
  ],
  "total": 1
}
```

### 6. Afficher les logs de connexion (GET)

```bash
curl http://localhost:5000/api/login-logs
```

**Réponse:**
```json
{
  "success": true,
  "logs": [
    {
      "id": 1,
      "email_or_phone": "jean@test.com",
      "success": 1,
      "ip_address": "127.0.0.1",
      "timestamp": "2026-03-24 10:32:15"
    }
  ],
  "total": 1
}
```

### 7. Afficher les statistiques (GET)

```bash
curl http://localhost:5000/api/stats
```

**Réponse:**
```json
{
  "success": true,
  "stats": {
    "total_users": 1,
    "total_login_attempts": 1,
    "successful_logins": 1,
    "total_connections": 1
  }
}
```

## 🔧 Tester avec Postman

1. Téléchargez [Postman](https://www.postman.com/downloads/)
2. Importez cet fichier ou créez des requêtes:

### Créer une nouvelle demande

**Signup:**
- URL: `http://localhost:5000/api/signup`
- Méthode: POST
- Body (JSON):
```json
{
  "firstname": "Test",
  "lastname": "User",
  "email": "test@example.com",
  "password": "password123",
  "birth_date": "1990-01-01",
  "gender": "Homme"
}
```

**Login:**
- URL: `http://localhost:5000/api/login`
- Méthode: POST
- Body (JSON):
```json
{
  "email_or_phone": "test@example.com",
  "password": "password123"
}
```

## 📝 Exemples complets

### Créer 3 utilisateurs de test

```bash
# Utilisateur 1
curl -X POST http://localhost:5000/api/signup -H "Content-Type: application/json" -d "{\"firstname\":\"Alice\",\"lastname\":\"Martin\",\"email\":\"alice@test.com\",\"password\":\"alice123\",\"birth_date\":\"1995-03-20\",\"gender\":\"Femme\"}"

# Utilisateur 2
curl -X POST http://localhost:5000/api/signup -H "Content-Type: application/json" -d "{\"firstname\":\"Bob\",\"lastname\":\"Bernard\",\"email\":\"bob@test.com\",\"password\":\"bob123\",\"birth_date\":\"1992-07-15\",\"gender\":\"Homme\"}"

# Utilisateur 3
curl -X POST http://localhost:5000/api/signup -H "Content-Type: application/json" -d "{\"firstname\":\"Charlie\",\"lastname\":\"Charles\",\"email\":\"charlie@test.com\",\"password\":\"charlie123\",\"birth_date\":\"1998-11-30\",\"gender\":\"Personnalisé\"}"
```

### Tenter une connexion réussie

```bash
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d "{\"email_or_phone\":\"alice@test.com\",\"password\":\"alice123\"}"
```

### Tenter une connexion échouée

```bash
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d "{\"email_or_phone\":\"alice@test.com\",\"password\":\"wrongpassword\"}"
```

### Voir tous les utilisateurs

```bash
curl http://localhost:5000/api/users | findstr .
```

### Voir toutes les données de connexion

```bash
curl http://localhost:5000/api/connection-data | findstr .
```

## 🐛 Débogage

### Voir les détails de la réponse avec les en-têtes

```bash
curl -i http://localhost:5000/api/users
```

### Sauvegarder la réponse dans un fichier

```bash
curl http://localhost:5000/api/users > response.json
```

### Afficher les logs du serveur

Regardez le terminal où `python app.py` s'exécute

## 📊 Analyse des données collectées

### Avec Python

```python
import sqlite3
import json

conn = sqlite3.connect('facebook.db')
cursor = conn.cursor()

# Voir tous les utilisateurs
cursor.execute('SELECT * FROM users')
print("=== UTILISATEURS ===")
for row in cursor.fetchall():
    print(row)

# Voir les données de connexion
cursor.execute('SELECT * FROM connection_data')
print("\n=== DONNÉES DE CONNEXION ===")
for row in cursor.fetchall():
    print(row)

conn.close()
```

### Avec le visualiseur Python

```bash
python view_data_simple.py
```

## ✅ Checklist de test

- [ ] Le serveur démarre sans erreur
- [ ] Inscription avec données valides fonctionne
- [ ] Inscription avec email déjà existant échoue
- [ ] Connexion avec les bonnes identifiants fonctionne
- [ ] Connexion avec les mauvais identifiants échoue
- [ ] Les données sont stockées dans la base de données
- [ ] Les données de connexion sont collectées
- [ ] Les statistiques sont mises à jour
- [ ] Les logs de connexion sont enregistrés

## Besoin d'aide?

Consultez:
- README.md - Documentation complète
- SETUP.md - Guide d'installation
- app.py - Code source du serveur
- script.js - Code source du frontend

---

**Happy Testing! 🧪**
