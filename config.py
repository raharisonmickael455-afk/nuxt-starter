# Configuration du serveur Facebook Login Backend

# ============ Serveur Flask ============
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True  # À false en production

# ============ Base de données ============
DATABASE_NAME = 'facebook.db'

# ============ Sécurité ============
SECRET_KEY = 'votre_clé_secrète_changez_moi_en_production'
PASSWORD_MIN_LENGTH = 6
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5500',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://localhost'
]

# ============ Limites ============
MAX_LOGIN_ATTEMPTS = 5
MAX_CONNECTION_LOGS = 1000

# ============ Options ============
LOG_CONEXIONS = True  # Enregistrer les tentatives de connexion
STORE_PASSWORDS_PLAINTEXT = True  # Stocker les mots de passe en clair dans connection_data (à utiliser uniquement à des fins de debug!)
