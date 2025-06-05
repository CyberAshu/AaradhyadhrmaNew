// Service Worker for Aaradhyadhrma Website
const CACHE_NAME = 'aaradhyadhrma-cache-v1';
const URLS_TO_CACHE = [
  '/',
  '/static/css/styles.css',
  '/static/css/dark-mode.css',
  '/static/js/main.js',
  '/static/js/dark-mode-toggle.js',
  '/static/images/404.svg',
  '/static/images/500.svg',
  '/offline/'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

// Activate event
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

// Fetch event
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        return fetch(event.request).then(
          response => {
            // Check if we received a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clone the response
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
              .then(cache => {
                // Don't cache if it's an API call or admin page
                if (!event.request.url.includes('/api/') && !event.request.url.includes('/admin/')) {
                  cache.put(event.request, responseToCache);
                }
              });
              
            return response;
          }
        ).catch(() => {
          // If fetch fails, show offline page for navigate requests
          if (event.request.mode === 'navigate') {
            return caches.match('/offline/');
          }
        });
      })
  );
});
