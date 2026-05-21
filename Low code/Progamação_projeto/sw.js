const CACHE_NAME = 'finance-v1';
const ASSETS = [
    './',
    './index.html',
    './app_icon_512x512_1767483499099.png'
];

self.addEventListener('install', (e) => {
    e.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', (e) => {
    e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
});
