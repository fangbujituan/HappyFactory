// StorageManager module - localStorage wrapper for game persistence

class StorageManager {
  constructor() {
    this.gameStateKey = 'gameState';
    this.bestScoreKey = 'bestScore';
    this.storageAvailable = this._testStorage();
  }

  /**
   * Test if localStorage is available (may be disabled in privacy mode).
   * @returns {boolean}
   */
  _testStorage() {
    try {
      var testKey = '__storage_test__';
      window.localStorage.setItem(testKey, '1');
      window.localStorage.removeItem(testKey);
      return true;
    } catch (e) {
      console.warn('localStorage is not available. Game will not persist state.');
      return false;
    }
  }

  /**
   * Read and parse a JSON value from localStorage.
   * Returns null if key is missing, storage unavailable, or data is corrupted.
   */
  _getItem(key) {
    if (!this.storageAvailable) {
      return null;
    }
    try {
      var data = window.localStorage.getItem(key);
      if (data === null) {
        return null;
      }
      return JSON.parse(data);
    } catch (e) {
      // Corrupted data — clear it and return null
      console.warn('Corrupted data for key "' + key + '". Clearing.');
      try {
        window.localStorage.removeItem(key);
      } catch (removeErr) {
        // Ignore — storage may have become unavailable
      }
      return null;
    }
  }

  /**
   * Write a JSON-serializable value to localStorage.
   */
  _setItem(key, value) {
    if (!this.storageAvailable) {
      return;
    }
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      // QuotaExceededError or other write failure — silently ignore
      console.warn('Failed to write to localStorage for key "' + key + '".');
    }
  }

  /**
   * Remove a key from localStorage.
   */
  _removeItem(key) {
    if (!this.storageAvailable) {
      return;
    }
    try {
      window.localStorage.removeItem(key);
    } catch (e) {
      // Ignore
    }
  }

  // ─── Public API ──────────────────────────────────────────────

  /**
   * Retrieve the saved game state, or null if none exists.
   */
  getGameState() {
    return this._getItem(this.gameStateKey);
  }

  /**
   * Persist the current game state.
   * @param {object} state - Serialized game state
   */
  setGameState(state) {
    this._setItem(this.gameStateKey, state);
  }

  /**
   * Clear the saved game state (e.g. on new game).
   */
  clearGameState() {
    this._removeItem(this.gameStateKey);
  }

  /**
   * Retrieve the best score, or 0 if none is stored.
   */
  getBestScore() {
    var score = this._getItem(this.bestScoreKey);
    return (typeof score === 'number' && score >= 0) ? score : 0;
  }

  /**
   * Persist the best score.
   * @param {number} score
   */
  setBestScore(score) {
    this._setItem(this.bestScoreKey, score);
  }
}

// Conditional export for Node.js/test environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { StorageManager };
}
