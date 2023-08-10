
const ServiceWorkerReg = async () => {
  console.log("[ServiceWorkerReg] enter")
  if ('serviceWorker' in navigator) {
    console.log("[ServiceWorkerReg] serviceworker in navigator")
    try {
      const params = new URLSearchParams(window.location.search);
      console.log("[ServiceWorkerReg] registering")

      const reg = await navigator.serviceWorker.register(
        `sw.js?user=${params.get("user") ?? 'stranger'}`,
        {
          scope: './',
        }
      );

      console.log("[ServiceWorkerReg] registered")
      console.log(reg)
      if (reg.installing) {
        console.log('Service worker installing');
      } else if (reg.waiting) {
        console.log('Service worker installed');
      } else if (reg.active) {
        console.log('Service worker active');
      }
    } catch (error) {
      console.error(`Registration failed with ${error}`);
    }
  }
  else {
    console.log("browser doesn't support sw")
  }
};

console.log("app.js")
ServiceWorkerReg();
