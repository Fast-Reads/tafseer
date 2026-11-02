const CACHE_NAME = 'tafseer-ahzab-v1';
const ASSETS = [
  './',
  './index.html',
  '../style.css',
  '../script.js',
  './manifest.json',
  '../icons/icon-192.png',
  '../icons/icon-512.png',
  './section-01.html',
  './section-02.html',
  './section-03.html',
  './section-04.html'
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

// Fetch: الشبكة أولاً للصفحات والأنماط والسكربتات حتى تصل التحديثات فوراً،
// والكاش أولاً لبقية الملفات (الأيقونات والخطوط) لأنها لا تتغيّر.
function isLive(url) {
  return url.origin === self.location.origin &&
         /\.(html|css|js)$|\/$/.test(url.pathname);
}

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  if (isLive(url)) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response && response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => caches.match(event.request)
          .then(cached => cached ||
            (event.request.mode === 'navigate' ? caches.match('./index.html') : undefined)))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response && response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      });
    }).catch(() => {
      if (event.request.mode === 'navigate') return caches.match('./index.html');
    })
  );
});
