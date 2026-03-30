// Grid module - manages the 4x4 grid data structure

class Grid {
  constructor(size = 4, previousState = null) {
    this.size = size;
    this.cells = previousState ? this.fromState(previousState) : this.empty();
  }

  // Create an empty grid
  empty() {
    var cells = [];
    for (var x = 0; x < this.size; x++) {
      var row = cells[x] = [];
      for (var y = 0; y < this.size; y++) {
        row.push(null);
      }
    }
    return cells;
  }

  // Restore grid from a previously serialized state
  fromState(state) {
    var cells = [];
    for (var x = 0; x < this.size; x++) {
      var row = cells[x] = [];
      for (var y = 0; y < this.size; y++) {
        var tileData = state[x][y];
        row.push(tileData ? new Tile(tileData.position, tileData.value) : null);
      }
    }
    return cells;
  }

  // Return all empty cell positions as [{x, y}, ...]
  emptyCells() {
    var cells = [];
    this.eachCell(function (x, y, tile) {
      if (!tile) {
        cells.push({ x: x, y: y });
      }
    });
    return cells;
  }

  // Return a random available cell position, or null if none
  randomAvailableCell() {
    var cells = this.emptyCells();
    if (cells.length) {
      return cells[Math.floor(Math.random() * cells.length)];
    }
    return null;
  }

  // Check if a position is within bounds and empty
  cellAvailable(pos) {
    return !this.cellOccupied(pos);
  }

  // Check if a position is occupied
  cellOccupied(pos) {
    return !!this.cellContent(pos);
  }

  // Return the tile at the given position, or null
  cellContent(pos) {
    if (this.withinBounds(pos)) {
      return this.cells[pos.x][pos.y];
    }
    return null;
  }

  // Check if a position is within grid bounds
  withinBounds(pos) {
    return pos.x >= 0 && pos.x < this.size &&
           pos.y >= 0 && pos.y < this.size;
  }

  // Insert a tile at its position
  insertTile(tile) {
    this.cells[tile.position.x][tile.position.y] = tile;
  }

  // Remove a tile from its position
  removeTile(tile) {
    this.cells[tile.position.x][tile.position.y] = null;
  }

  // Iterate over all cells, calling callback(x, y, tile) for each
  eachCell(callback) {
    for (var x = 0; x < this.size; x++) {
      for (var y = 0; y < this.size; y++) {
        callback(x, y, this.cells[x][y]);
      }
    }
  }

  // Serialize grid to a plain data object
  serialize() {
    var cellState = [];
    for (var x = 0; x < this.size; x++) {
      var row = cellState[x] = [];
      for (var y = 0; y < this.size; y++) {
        row.push(this.cells[x][y] ? this.cells[x][y].serialize() : null);
      }
    }
    return {
      size: this.size,
      cells: cellState
    };
  }
}

// Conditional export for Node.js/test environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Grid };
}
