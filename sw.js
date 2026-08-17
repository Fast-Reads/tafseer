const CACHE_NAME = 'tafseer-baqarah-v4';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './section-01.html',
  './section-02.html',
  './section-03.html',
  './section-04.html',
  './section-05.html',
  './section-06.html',
  './section-07.html',
  './section-08.html',
  './section-09.html',
  './section-10.html',
  './section-11.html',
  './section-12.html',
  './section-13.html',
  './section-14.html',
  './section-15.html',
  './section-16.html',
  './section-17.html',
  './section-18.html',
  './section-19.html',
  './section-20.html',
  './section-21.html'
];

// Install: cache all assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: serve from cache, fall back to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          // Cache new requests (like Google Fonts)
          if (response.ok && event.request.method === 'GET') {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
      .catch(() => {
        // Offline fallback for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      })
  );
});
