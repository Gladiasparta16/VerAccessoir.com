(function () {
  // Utility to safely read/write JSON from localStorage
  const logger = (msg, err) => { try { console.error(msg, err); } catch (e) {} };

  function getJSON(key, defaultValue) {
    try {
      const v = localStorage.getItem(key);
      if (!v) return defaultValue;
      return JSON.parse(v);
    } catch (e) {
      logger(`Erreur parsing localStorage key ${key}:`, e);
      return defaultValue;
    }
  }

  function setJSON(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      logger(`Erreur saving localStorage key ${key}:`, e);
    }
  }

  // Expose globally
  window.storage = window.storage || {};
  window.storage.getJSON = getJSON;
  window.storage.setJSON = setJSON;
})();