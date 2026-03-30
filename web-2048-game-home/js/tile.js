// Tile module - represents a single numbered tile on the grid

class Tile {
  constructor(position, value = 2) {
    this.position = { x: position.x, y: position.y };
    this.value = value;
    this.previousPosition = null;
    this.mergedFrom = null;
  }

  // Save current position to previousPosition (used for animation)
  savePosition() {
    this.previousPosition = { x: this.position.x, y: this.position.y };
  }

  // Update tile position
  updatePosition(pos) {
    this.position = { x: pos.x, y: pos.y };
  }

  // Serialize tile to plain object
  serialize() {
    return {
      position: { x: this.position.x, y: this.position.y },
      value: this.value
    };
  }
}

// Conditional export for Node.js/test environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Tile };
}
