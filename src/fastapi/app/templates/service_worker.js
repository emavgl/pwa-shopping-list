const CACHE_NAME = 'shopping-list-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Only process requests that have a "list" parameter
  if (url.searchParams.has('list')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          // Cache hit - return response
          if (response) {
            return response;
          }

          // Clone the request since it's one-time use
          const fetchRequest = event.request.clone();

          return fetch(fetchRequest).then(
            response => {
              // Check if we received a valid response
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }

              // Clone the response because it's one-time use
              const responseToCache = response.clone();

              caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, responseToCache);
              });

              return response;
            }
          );
        })
    );
  } else {
    // If the request does NOT have a "list" parameter, fetch normally (no caching)
    event.respondWith(fetch(event.request));
  }
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});