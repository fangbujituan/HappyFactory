// UIRenderer module - renders game state to the DOM

class UIRenderer {
  constructor() {
    this.tileContainer = document.querySelector('.tile-container');
    this.scoreDisplay = document.querySelector('.score-value');
    this.bestDisplay = document.querySelector('.best-value');
    this.messageContainer = document.querySelector('.game-message');
    this.messageText = document.querySelector('.game-message p');
  }

  /**
   * Render the grid to the DOM.
   * Accepts a Grid instance (with live Tile objects for animation metadata).
   */
  render(grid) {
    // Clear all existing tile elements
    while (this.tileContainer.firstChild) {
      this.tileContainer.removeChild(this.tileContainer.firstChild);
    }

    grid.eachCell(function (x, y, tile) {
      if (tile) {
        this.addTile(tile);
      }
    }.bind(this));
  }

  /**
   * Create and append a DOM element for a single tile.
   */
  addTile(tile) {
    var element = document.createElement('div');
    var position = tile.position;
    var value = tile.value;

    // Base classes — add tile-super for values beyond 2048
    var classes = ['tile', 'tile-' + value];
    if (value > 2048) {
      classes.push('tile-super');
    }

    if (tile.previousPosition) {
      // Tile moved: start at previous position, then animate to new position
      var prevClass = this.positionClass(tile.previousPosition);
      classes.push(prevClass);
      element.className = classes.join(' ');

      // Use requestAnimationFrame to trigger CSS transition
      var self = this;
      requestAnimationFrame(function () {
        element.classList.remove(prevClass);
        element.classList.add(self.positionClass(position));
      });
    } else {
      // New tile or restored tile — place directly
      classes.push(this.positionClass(position));

      if (tile.mergedFrom) {
        classes.push('tile-merged');
      } else {
        classes.push('tile-new');
      }

      element.className = classes.join(' ');
    }

    // If tile was merged, also add merged class after positioning
    if (tile.previousPosition && tile.mergedFrom) {
      element.classList.add('tile-merged');
    }

    element.textContent = value;
    this.tileContainer.appendChild(element);
  }

  /**
   * Return the 1-indexed position class string for CSS grid placement.
   */
  positionClass(pos) {
    return 'tile-position-' + (pos.x + 1) + '-' + (pos.y + 1);
  }

  /**
   * Update the current score display.
   */
  updateScore(score) {
    this.scoreDisplay.textContent = score;
  }

  /**
   * Update the best score display.
   */
  updateBestScore(best) {
    this.bestDisplay.textContent = best;
  }

  /**
   * Show the game over or win message overlay.
   * @param {boolean} won - true if player won, false if game over
   */
  showMessage(won) {
    this.messageText.textContent = won ? '你赢了！' : '游戏结束！';
    this.messageContainer.classList.add('active');
  }

  /**
   * Clear the message overlay.
   */
  clearMessage() {
    this.messageContainer.classList.remove('active');
  }
}
