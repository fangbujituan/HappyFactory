// InputHandler module - handles keyboard and touch input

class InputHandler {
  constructor(callbacks) {
    this.callbacks = callbacks; // { move: fn(direction), restart: fn(), keepPlaying: fn() }
    this.touchStartX = 0;
    this.touchStartY = 0;

    this.listen();
  }

  listen() {
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleTouchStart = this.handleTouchStart.bind(this);
    this.handleTouchEnd = this.handleTouchEnd.bind(this);

    document.addEventListener('keydown', this.handleKeyDown);

    var gameContainer = document.querySelector('.game-container');
    if (gameContainer) {
      gameContainer.addEventListener('touchstart', this.handleTouchStart);
      gameContainer.addEventListener('touchend', this.handleTouchEnd);
    }

    this.bindButtonEvents();
  }

  handleKeyDown(event) {
    var keyMap = {
      ArrowUp: 0,    // up
      ArrowRight: 1,  // right
      ArrowDown: 2,   // down
      ArrowLeft: 3    // left
    };

    var direction = keyMap[event.key];

    if (direction !== undefined) {
      event.preventDefault();
      if (this.callbacks.move) {
        this.callbacks.move(direction);
      }
    }
  }

  handleTouchStart(event) {
    if (event.touches && event.touches.length > 0) {
      this.touchStartX = event.touches[0].clientX;
      this.touchStartY = event.touches[0].clientY;
    }
  }

  handleTouchEnd(event) {
    if (!event.changedTouches || event.changedTouches.length === 0) {
      return;
    }

    var touchEndX = event.changedTouches[0].clientX;
    var touchEndY = event.changedTouches[0].clientY;

    var dx = touchEndX - this.touchStartX;
    var dy = touchEndY - this.touchStartY;

    var absDx = Math.abs(dx);
    var absDy = Math.abs(dy);

    // Only trigger if swipe distance > 30px
    if (Math.max(absDx, absDy) <= 30) {
      return;
    }

    var direction;

    if (absDx >= absDy) {
      // Horizontal swipe
      direction = dx > 0 ? 1 : 3; // right : left
    } else {
      // Vertical swipe
      direction = dy > 0 ? 2 : 0; // down : up
    }

    if (this.callbacks.move) {
      this.callbacks.move(direction);
    }
  }

  bindButtonEvents() {
    // New game button
    var newGameButton = document.querySelector('.new-game-button');
    if (newGameButton) {
      newGameButton.addEventListener('click', function () {
        if (this.callbacks.restart) {
          this.callbacks.restart();
        }
      }.bind(this));
    }

    // Retry button (in game over message)
    var retryButton = document.querySelector('.retry-button');
    if (retryButton) {
      retryButton.addEventListener('click', function () {
        if (this.callbacks.restart) {
          this.callbacks.restart();
        }
      }.bind(this));
    }

    // Keep playing button (in win message)
    var keepPlayingButton = document.querySelector('.keep-playing-button');
    if (keepPlayingButton) {
      keepPlayingButton.addEventListener('click', function () {
        if (this.callbacks.keepPlaying) {
          this.callbacks.keepPlaying();
        }
      }.bind(this));
    }
  }
}
