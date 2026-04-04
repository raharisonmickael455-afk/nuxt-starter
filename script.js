// Éléments du formulaire de connexion
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');
const loginBtn = loginForm.querySelector('.login-btn');
const createAccountBtn = document.querySelector('.create-account-btn');

// Éléments du modal
const signupModal = document.getElementById('signupModal');
const signupForm = document.getElementById('signupForm');
const closeModal = document.getElementById('closeModal');
const forgotLink = document.getElementById('forgotLink');

// ============ VALIDATION ============

// Valider email
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$|^\d{10,}$/;
    return regex.test(email);
}

// Valider mot de passe
function validatePassword(password) {
    return password.length >= 6;
}

// Afficher les erreurs
function showError(inputField, errorElement, message) {
    inputField.classList.add('error');
    errorElement.textContent = message;
}

// Masquer les erreurs
function clearError(inputField, errorElement) {
    inputField.classList.remove('error');
    errorElement.textContent = '';
}

// Validation en temps réel
emailInput.addEventListener('input', () => {
    if (emailInput.value.trim() === '') {
        clearError(emailInput, emailError);
    } else if (!validateEmail(emailInput.value)) {
        showError(emailInput, emailError, 'Email ou numéro invalide');
    } else {
        clearError(emailInput, emailError);
    }
});

passwordInput.addEventListener('input', () => {
    if (passwordInput.value === '') {
        clearError(passwordInput, passwordError);
    } else if (!validatePassword(passwordInput.value)) {
        showError(passwordInput, passwordError, 'Le mot de passe doit contenir au moins 6 caractères');
    } else {
        clearError(passwordInput, passwordError);
    }
});

// ============ SOUMISSION DU FORMULAIRE DE CONNEXION ============

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Réinitialiser les erreurs
    clearError(emailInput, emailError);
    clearError(passwordInput, passwordError);

    let hasError = false;

    // Valider email
    if (emailInput.value.trim() === '') {
        showError(emailInput, emailError, 'Veuillez entrer votre email');
        hasError = true;
    } else if (!validateEmail(emailInput.value)) {
        showError(emailInput, emailError, 'Email ou numéro invalide');
        hasError = true;
    }

    // Valider mot de passe
    if (passwordInput.value === '') {
        showError(passwordInput, passwordError, 'Veuillez entrer votre mot de passe');
        hasError = true;
    } else if (!validatePassword(passwordInput.value)) {
        showError(passwordInput, passwordError, 'Le mot de passe doit contenir au moins 6 caractères');
        hasError = true;
    }

    // Si pas d'erreur
    if (!hasError) {
        loginBtn.disabled = true;
        loginBtn.textContent = 'Connexion...';

        try {
            // Envoyer les données au serveur Python
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email_or_phone: emailInput.value.trim(),
                    password: passwordInput.value
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                console.log('✓ Connexion réussie depuis le serveur!', data);
                alert(`✓ Connexion réussie!\nBienvenue ${data.user.firstname}!\n\nVos données ont été envoyées au serveur`);
                loginForm.reset();
            } else {
                console.error('✗ Erreur de connexion:', data.message);
                showError(emailInput, emailError, data.message || 'Erreur de connexion');
            }
        } catch (error) {
            console.error('Erreur réseau:', error);
            alert('⚠️  Impossible de se connecter au serveur Python.\nAssurez-vous que le serveur est en cours d\'exécution sur le port 5000.\n\nLancez: python app.py');
        } finally {
            loginBtn.disabled = false;
            loginBtn.textContent = 'Se connecter';
        }
    }
});

// ============ MODAL D'INSCRIPTION ============

// Ouvrir le modal
createAccountBtn.addEventListener('click', (e) => {
    e.preventDefault();
    signupModal.classList.add('active');
});

// Fermer le modal
closeModal.addEventListener('click', () => {
    signupModal.classList.remove('active');
});

// Fermer le modal en cliquant en dehors
window.addEventListener('click', (e) => {
    if (e.target === signupModal) {
        signupModal.classList.remove('active');
    }
});

// ============ SOUMISSION DU FORMULAIRE D'INSCRIPTION ============

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const signupEmail = document.getElementById('signupEmail').value.trim();
    const signupPassword = document.getElementById('signupPassword').value;
    const birthDate = document.getElementById('birthDate').value;
    const gender = document.querySelector('input[name="gender"]:checked');

    // Validation
    let isValid = true;

    if (firstName === '') {
        alert('Veuillez entrer votre prénom');
        isValid = false;
    } else if (lastName === '') {
        alert('Veuillez entrer votre nom');
        isValid = false;
    } else if (!validateEmail(signupEmail)) {
        alert('Veuillez entrer une adresse email valide');
        isValid = false;
    } else if (!validatePassword(signupPassword)) {
        alert('Le mot de passe doit contenir au moins 6 caractères');
        isValid = false;
    } else if (birthDate === '') {
        alert('Veuillez entrer votre date de naissance');
        isValid = false;
    } else if (!gender) {
        alert('Veuillez sélectionner votre sexe');
        isValid = false;
    }

    // Si valide, envoyer au serveur
    if (isValid) {
        const signupBtn = signupForm.querySelector('.login-btn');
        signupBtn.disabled = true;
        signupBtn.textContent = "S'inscrivant...";

        try {
            // Envoyer les données au serveur Python
            const response = await fetch('http://localhost:5000/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    firstname: firstName,
                    lastname: lastName,
                    email: signupEmail,
                    password: signupPassword,
                    birth_date: birthDate,
                    gender: gender.value
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                console.log('✓ Inscription réussie depuis le serveur!', data);
                alert(`✓ Inscription réussie!\nBienvenue ${firstName}!\n\nVos données ont été enregistrées dans la base de données`);
                signupForm.reset();
                signupModal.classList.remove('active');
            } else {
                console.error('✗ Erreur lors de l\'inscription:', data.message);
                alert(`⚠️  ${data.message}`);
            }
        } catch (error) {
            console.error('Erreur réseau:', error);
            alert('⚠️  Impossible de se connecter au serveur Python.\nAssurez-vous que le serveur est en cours d\'exécution sur le port 5000.\n\nLancez: python app.py');
        } finally {
            signupBtn.disabled = false;
            signupBtn.textContent = "S'inscrire";
        }
    }
});

// ============ MOT DE PASSE OUBLIÉ ============

forgotLink.addEventListener('click', (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    
    if (!email) {
        alert('Veuillez d\'abord entrer votre email');
        emailInput.focus();
    } else if (!validateEmail(email)) {
        alert('Veuillez entrer une adresse email valide');
    } else {
        alert(`Un lien de réinitialisation\n\nsi été envoyé à: ${email}\n\nNote: Ceci est une démonstration`);
    }
});

// ============ AMÉLIORATIONS UX ============

// Appuyer sur Entrée pour soumettre
passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loginForm.dispatchEvent(new Event('submit'));
    }
});

// Ajouter des animations de focus
document.querySelectorAll('.input-field').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.01)';
    });

    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// ============ LOCAL STORAGE ============

// Sauvegarder les préférences
function savePreferences() {
    const preferences = {
        rememberEmail: emailInput.value,
        timestamp: new Date().getTime()
    };
    localStorage.setItem('fbLoginPreferences', JSON.stringify(preferences));
}

// Charger les préférences
function loadPreferences() {
    const saved = localStorage.getItem('fbLoginPreferences');
    if (saved) {
        const preferences = JSON.parse(saved);
        // Commenter cette ligne si vous ne voulez pas charger automatiquement l'email
        // emailInput.value = preferences.rememberEmail;
    }
}

// Charger les préférences au chargement de la page
window.addEventListener('load', loadPreferences);

// Sauvegarder les préférences avant de quitter
window.addEventListener('beforeunload', savePreferences);

// ============ OPTIMISATION MOBILE ============

// Empêcher le zoom sur les inputs
document.addEventListener('touchstart', (e) => {
    if (e.target.matches('input, textarea, select, button')) {
        e.target.style.fontSize = '16px';
    }
});

// Améliorer les interactions tactiles
document.querySelectorAll('button, input, .forgot-password a').forEach(element => {
    element.addEventListener('touchstart', function() {
        this.style.opacity = '0.8';
    });
    element.addEventListener('touchend', function() {
        this.style.opacity = '1';
    });
});

// Détection des changements d'orientation
window.addEventListener('orientationchange', () => {
    // Ajuster le layout si nécessaire
    setTimeout(() => {
        window.scrollTo(0, 0);
    }, 100);
});

// Service Worker pour PWA (offline support)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
        .then(registration => {
            console.log('✓ Service Worker enregistré');
        })
        .catch(error => {
            console.log('Service Worker non disponible:', error);
        });
}

// Notification para PWA
if ('Notification' in window && Notification.permission === 'granted') {
    console.log('✓ Notifications actives');
}

console.log('✓ Page de connexion Facebook chargée avec succès!');
console.log('📱 Compatible avec tous les appareils (mobile, tablet, desktop)');
