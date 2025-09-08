// frontend/sw.js
const CACHE_NAME = 'health-chatbot-v1';
const urlsToCache = [
  '/',
  '/css/tailwind.css',
  '/js/chat.js',
  '/js/quiz.js',
  '/js/offline.js',
  '/assets/bot-avatar.png',
  '/assets/favicon.ico'
];

// Install service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch events
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
  );
});