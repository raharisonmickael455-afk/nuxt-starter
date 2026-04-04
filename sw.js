// Service Worker pour Facebook Login - Supp offline et caching

const CACHE_NAME = 'facebook-login-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './styles.css',
    './script.js',
    './manifest.json',
    'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192"><rect fill="%230a66c2" width="192" height="192"/><text x="96" y="140" font-size="120" font-weight="bold" fill="white" text-anchor="middle">f</text></svg>'
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('✓ Cache setup complété');
            return cache.addAll(ASSETS_TO_CACHE).catch((error) => {
                console.log('Avertissement: Certains assets n\'ont pas pu être cachés', error);
            });
        })
    );
    self.skipWaiting();
});

// Activation
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Suppression de l\'ancien cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch - Cache First pour les assets, Network First pour l'API
self.addEventListener('fetch', (event) => {
    // Ne pas mettre en cache les requêtes API
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => response)
                .catch(() => {
                    return caches.match('./index.html');
                })
        );
        return;
    }

    // Cache First pour les assets statiques
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }
                return fetch(event.request)
                    .then((response) => {
                        if (!response || response.status !== 200 || response.type === 'error') {
                            return response;
                        }
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                        return response;
                    })
                    .catch(() => {
                        // En cas d'erreur réseau, retourner la page d'accueil
                        return caches.match('./index.html');
                    });
            })
    );
});

// Message depuis le client
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

console.log('✓ Service Worker activé');
