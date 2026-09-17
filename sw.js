/* Deep Pocket — service worker.
 * Scope is / by virtue of this file's location.
 *
 * Bump CACHE on every release. The old cache is deleted on activate, so a
 * stale build can never outlive one launch.
 */
var CACHE = "deep-pocket-v43";

/* The shell — everything needed to open and show a UI with no network. */
var SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-180.png",
  "./icon-192.png",
  "./icon-512.png",
  "./kits/kits.json"
];

self.addEventListener("install", function (e) {
  /* Do NOT skipWaiting: a new worker taking over mid-loop would swap the
     sample cache under a running transport. The update lands on next launch. */
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      /* addAll is all-or-nothing; one 404 would fail the whole install and
         leave the app with no worker at all. Add individually and survive. */
      return Promise.all(SHELL.map(function (u) {
        return c.add(u).catch(function () { /* logged by the page, not fatal */ });
      }));
    })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k.startsWith("deep-pocket-") && k !== CACHE) return caches.delete(k);
        return null;
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;

  var url = new URL(req.url);
  if (url.origin !== location.origin) return;          /* never touch third parties */
  if (!url.pathname.startsWith("/")) return; /* belt and braces on scope */
  /* Icons and the manifest go straight to the network, never through this
     worker. iOS builds the Home Screen tile from them in a separate loader;
     with this worker answering them, iOS showed a letter tile ("D") — suspected cause, 2026-09-16. */
  if (/\.(png|webmanifest)$/i.test(url.pathname)) return;

  /* Samples: cache-first, forever. 5.3 MB of FLAC across 137 files is the
     whole reason this worker exists — it must be fetched once, not once a day. */
  if (/\.(flac|wav|ogg|mp3|m4a)$/i.test(url.pathname)) {
    e.respondWith(
      caches.match(req).then(function (hit) {
        if (hit) return hit;
        return fetch(req).then(function (res) {
          if (res && res.ok) {
            var copy = res.clone();
            caches.open(CACHE).then(function (c) { c.put(req, copy); });
          }
          return res;
        });
      })
    );
    return;
  }

  /* Everything else — the page, the manifest, the icons: network first so a
     new build is picked up, cache as the fallback so no network still opens.
     3 s is long enough for a good connection and short enough to not feel broken. */
  e.respondWith(
    new Promise(function (resolve) {
      var settled = false;
      var done = function (r) { if (!settled) { settled = true; resolve(r); } };
      var timer = setTimeout(function () {
        caches.match(req).then(function (hit) { if (hit) done(hit); });
      }, 3000);

      fetch(req).then(function (res) {
        clearTimeout(timer);
        if (res && res.ok) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        done(res);
      }).catch(function () {
        clearTimeout(timer);
        caches.match(req).then(function (hit) {
          done(hit || new Response("", { status: 504, statusText: "offline" }));
        });
      });
    })
  );
});
