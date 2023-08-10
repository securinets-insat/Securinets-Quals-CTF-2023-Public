
const params = new URLSearchParams(self.location.search)
const userId = params.get("user")
const serverURL = `https://testnos.e-health.software/GetToken?userid=${userId}`;
async function getToken() {
  const myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');


  const myRequest = new Request(serverURL, {
    method: 'GET',
    headers: myHeaders,
  });

  try {
    const response = await fetch(myRequest);

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const responseFromCache = await caches.match(myRequest);

    if (responseFromCache) {
      const data = await responseFromCache.json();
      return data.token;
    }
    putInCache(myRequest, response.clone())
    const data = await response.json();
    return data.token;
  } catch (error) {
    console.error('Error fetching token:', error.message);
    return null;
  }
}

async function fetchDataWithToken(token, url) {
  try {
    const auth = `Auth-Token-${userId}`
    const headers = {}
    headers[auth] = token
    const response = await fetch(url, {
      method: 'GET',
      headers: headers,
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return response
  } catch (error) {
    console.error('Error fetching data with token:', error);
  }
}



const addResourcesToCache = async (resources) => {
  const cache = await caches.open('v1');

  await cache.addAll(resources);
};

const putInCache = async (request, response) => {
  if ((request.url.indexOf('http') === -1)) return;
  const cache = await caches.open('v1');
  await cache.put(request, response);
};
const cacheFirst = async ({ request, preloadResponsePromise, fallbackUrl }) => {
  if ((request.url.indexOf('http') === -1)) return;
  const responseFromCache = await caches.match(request);
  if (responseFromCache) {
    return responseFromCache;
  }

  const preloadResponse = await preloadResponsePromise;
  if (preloadResponse) {

    console.info('using preload response', preloadResponse);
    putInCache(request, preloadResponse.clone());
    return preloadResponse;
  }

  try {

    const token = await getToken()
    const responseFromNetwork = await fetchDataWithToken(token, request.clone());
    putInCache(request, responseFromNetwork.clone());
    return responseFromNetwork;

  } catch (error) {
    console.log(error)
    const fallbackResponse = await caches.match(fallbackUrl);
    if (fallbackResponse) {
      return fallbackResponse;
    }
    return new Response('Network error happened', {
      status: 408,
      headers: { 'Content-Type': 'text/plain' },
    });
  }
};

const enableNavigationPreload = async () => {
  if (self.registration.navigationPreload) {

    await self.registration.navigationPreload.enable();
  }
};

self.addEventListener('activate', (event) => {
  event.waitUntil(enableNavigationPreload());
});

self.addEventListener('install', (event) => {

  event.waitUntil(async () => {
    await addResourcesToCache([
      './',
      './index.html',
      './style.css',
      './app.js',
      './securinets.html',
      './helloworld.html',
      './purify.js',
      './securinets.png',

    ])


  }


  );
});

self.addEventListener('fetch', (event) => {
  let req = null
  if (event.request.url.endsWith('/GetToken')) {
    req = new Request(serverURL, event.request)
  }

  event.respondWith(
    cacheFirst({
      request: req ?? event.request,
      preloadResponsePromise: event.preloadResponse,
      fallbackUrl: './securinets.png',
    })
  );
});
