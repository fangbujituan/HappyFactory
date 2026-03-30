// App entry point - initializes and connects all modules

document.addEventListener('DOMContentLoaded', function () {
  // 1. Instantiate core modules
  var storageManager = new StorageManager();
  var renderer = new UIRenderer();

  // 2. Create GameManager (auto-restores from save or starts new game)
  var gameManager = new GameManager(4, renderer, storageManager);

  // 3. Input queue mechanism for handling inputs during animation
  var isAnimating = false;
  var inputQueue = [];
  var ANIMATION_DURATION = 150; // ms, matches CSS transition duration

  function processMove(direction) {
    if (isAnimating) {
      // Queue the input while animation is in progress
      inputQueue.push(direction);
      return;
    }

    isAnimating = true;
    gameManager.move(direction);

    // After animation duration, process next queued input or release lock
    setTimeout(function drainQueue() {
      if (inputQueue.length > 0) {
        var next = inputQueue.shift();
        gameManager.move(next);
        setTimeout(drainQueue, ANIMATION_DURATION);
      } else {
        isAnimating = false;
      }
    }, ANIMATION_DURATION);
  }

  // 4. Connect InputHandler with callbacks
  var inputHandler = new InputHandler({
    move: function (direction) {
      processMove(direction);
    },
    restart: function () {
      // Clear queue and animation state on restart
      inputQueue = [];
      isAnimating = false;
      gameManager.setup();
    },
    keepPlaying: function () {
      gameManager.continueGame();
    }
  });
});
