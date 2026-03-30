// GameManager module - core game controller

/**
 * Move and merge a single line to the left.
 * Pure function: takes an array of tile values (0 = empty),
 * returns { line: [...], score: number }.
 *
 * Algorithm:
 *   1. Filter out zeros (empty cells)
 *   2. Scan left-to-right, merging adjacent equal values
 *      (a merged tile is skipped so it won't merge again)
 *   3. Pad with zeros to the original length
 */
function moveLine(line) {
  var length = line.length;
  // Step 1 – keep only non-zero values
  var filtered = line.filter(function (v) { return v !== 0; });

  // Step 2 – merge adjacent equal values from left to right
  var merged = [];
  var score = 0;
  var i = 0;
  while (i < filtered.length) {
    if (i + 1 < filtered.length && filtered[i] === filtered[i + 1]) {
      var newValue = filtered[i] * 2;
      merged.push(newValue);
      score += newValue;
      i += 2; // skip both tiles; the merged result won't merge again
    } else {
      merged.push(filtered[i]);
      i += 1;
    }
  }

  // Step 3 – pad with zeros to restore original length
  while (merged.length < length) {
    merged.push(0);
  }

  return { line: merged, score: score };
}

/**
 * Transpose a 2D grid (swap rows and columns).
 * cells[x][y] becomes cells[y][x].
 * Returns a new 2D array.
 */
function transposeGrid(grid) {
  var size = grid.length;
  var result = [];
  for (var x = 0; x < size; x++) {
    result[x] = [];
    for (var y = 0; y < size; y++) {
      result[x][y] = grid[y][x];
    }
  }
  return result;
}

/**
 * Reverse each row of a 2D grid.
 * Returns a new 2D array with each inner array reversed.
 */
function reverseRows(grid) {
  var result = [];
  for (var i = 0; i < grid.length; i++) {
    result[i] = grid[i].slice().reverse();
  }
  return result;
}

/**
 * Extract a value-only 2D array from a Grid instance, organized by rows.
 * Returns rows[y][x] so that each inner array is a visual row (left to right).
 * This makes "move left" = moveLine on each row directly.
 */
function gridToRows(grid) {
  var size = grid.size;
  var rows = [];
  for (var y = 0; y < size; y++) {
    rows[y] = [];
    for (var x = 0; x < size; x++) {
      var tile = grid.cells[x][y];
      rows[y][x] = tile ? tile.value : 0;
    }
  }
  return rows;
}

/**
 * Apply the full move algorithm to a Grid instance in the given direction.
 * Uses coordinate transforms to unify all 4 directions into "move left".
 *
 * Direction mapping: 0=up, 1=right, 2=down, 3=left
 *
 * Transform strategy:
 *   Left  (3): move left directly
 *   Right (1): reverse rows → move left → reverse rows
 *   Up    (0): transpose → move left → transpose
 *   Down  (2): transpose → reverse rows → move left → reverse rows → transpose
 *
 * Returns { values: 2D array of new values, score: total merge score, moved: boolean }
 */
function applyMove(grid, direction) {
  var rows = gridToRows(grid);
  var size = grid.size;

  // Pre-transform based on direction
  if (direction === 0) {
    // Up: transpose so columns become rows, then move left = move up
    rows = transposeGrid(rows);
  } else if (direction === 1) {
    // Right: reverse each row, then move left = move right
    rows = reverseRows(rows);
  } else if (direction === 2) {
    // Down: transpose then reverse, then move left = move down
    rows = transposeGrid(rows);
    rows = reverseRows(rows);
  }
  // Left (3): no transform needed

  // Apply moveLine to each row (move left)
  var totalScore = 0;
  var newRows = [];
  for (var i = 0; i < size; i++) {
    var result = moveLine(rows[i]);
    newRows[i] = result.line;
    totalScore += result.score;
  }

  // Post-transform (inverse of pre-transform)
  if (direction === 0) {
    // Up: transpose back
    newRows = transposeGrid(newRows);
  } else if (direction === 1) {
    // Right: reverse rows back
    newRows = reverseRows(newRows);
  } else if (direction === 2) {
    // Down: reverse rows back then transpose back
    newRows = reverseRows(newRows);
    newRows = transposeGrid(newRows);
  }
  // Left (3): no inverse transform needed

  // Detect if anything changed by comparing with original rows
  var originalRows = gridToRows(grid);
  var moved = false;
  for (var y = 0; y < size && !moved; y++) {
    for (var x = 0; x < size && !moved; x++) {
      if (originalRows[y][x] !== newRows[y][x]) {
        moved = true;
      }
    }
  }

  return { rows: newRows, score: totalScore, moved: moved };
}

/**
 * Build traversal orders for iterating over the grid in a given direction.
 * Returns { x: [...], y: [...] } arrays indicating the order to visit cells.
 *
 * Direction mapping: 0=up, 1=right, 2=down, 3=left
 *
 * For directions that move toward higher indices (right, down),
 * we traverse in reverse order so tiles are processed from the far edge first.
 */
function buildTraversals(direction, size) {
  var xs = [];
  var ys = [];
  for (var i = 0; i < size; i++) {
    xs.push(i);
    ys.push(i);
  }

  // Right (1): traverse x in reverse
  if (direction === 1) {
    xs = xs.reverse();
  }
  // Down (2): traverse y in reverse
  if (direction === 2) {
    ys = ys.reverse();
  }

  return { x: xs, y: ys };
}

/**
 * Generate a new random tile (value 2 at 90% probability, 4 at 10%)
 * and insert it into the grid at a random empty cell.
 * Returns the new Tile, or null if no empty cell is available.
 */
function addRandomTile(grid) {
  var cell = grid.randomAvailableCell();
  if (cell) {
    var value = Math.random() < 0.9 ? 2 : 4;
    var tile = new Tile(cell, value);
    grid.insertTile(tile);
    return tile;
  }
  return null;
}

// ─── GameManager class ───────────────────────────────────────────────

class GameManager {
  /**
   * @param {number} size - Grid size (default 4)
   * @param {object|null} renderer - UIRenderer instance (may be null)
   * @param {object|null} storageManager - StorageManager instance (may be null)
   */
  constructor(size, renderer, storageManager) {
    this.size = size || 4;
    this.renderer = renderer || null;
    this.storageManager = storageManager || null;

    this.grid = null;
    this.score = 0;
    this.bestScore = 0;
    this.over = false;
    this.won = false;
    this.keepPlaying = false;

    // Load best score from storage if available
    if (this.storageManager) {
      this.bestScore = this.storageManager.getBestScore() || 0;
    }

    // Try to restore previous game state, otherwise start fresh
    var previousState = null;
    if (this.storageManager) {
      previousState = this.storageManager.getGameState();
    }

    if (previousState) {
      this.grid = new Grid(previousState.grid.size, previousState.grid.cells);
      this.score = previousState.score;
      this.over = previousState.over;
      this.won = previousState.won;
      this.keepPlaying = previousState.keepPlaying || false;
      this.actuate();
    } else {
      this.setup();
    }
  }

  /**
   * Initialize or restart the game: clear grid, reset score,
   * generate 2 initial tiles, notify renderer.
   */
  setup() {
    this.grid = new Grid(this.size);
    this.score = 0;
    this.over = false;
    this.won = false;
    this.keepPlaying = false;

    // Generate 2 initial tiles
    addRandomTile(this.grid);
    addRandomTile(this.grid);

    // Clear saved game state
    if (this.storageManager) {
      this.storageManager.clearGameState();
    }

    this.actuate();
  }

  /**
   * Return a snapshot of the current game state.
   */
  getState() {
    return {
      grid: this.grid.serialize(),
      score: this.score,
      bestScore: this.bestScore,
      over: this.over,
      won: this.won,
      keepPlaying: this.keepPlaying
    };
  }

  /**
   * Execute a move in the given direction.
   * Direction mapping: 0=up, 1=right, 2=down, 3=left
   */
  move(direction) {
    // Block moves if game is over or won (unless keepPlaying)
    if (this.over || (this.won && !this.keepPlaying)) {
      return;
    }

    // Save all current tile positions for animation tracking
    this.prepareTiles();

    // Apply the move algorithm to get new grid values
    var result = applyMove(this.grid, direction);

    if (result.moved) {
      // Rebuild the grid with new Tile objects, tracking animation metadata
      this.rebuildGrid(result.rows);

      // Add a random tile to an empty cell
      var newTile = addRandomTile(this.grid);
      if (newTile) {
        newTile.previousPosition = null; // mark as new (no previous position)
      }

      // Update score
      this.score += result.score;
      if (this.score > this.bestScore) {
        this.bestScore = this.score;
        if (this.storageManager) {
          this.storageManager.setBestScore(this.bestScore);
        }
      }

      // Check for 2048 tile (win condition)
      if (!this.won && this.hasTileValue(2048)) {
        this.won = true;
      }

      // Check for game over
      if (this.isGameOver()) {
        this.over = true;
      }
    }

    // Notify renderer and save state regardless of whether move was valid
    this.actuate();
    this.saveState();
  }

  /**
   * Save current position of every tile to previousPosition (for animation).
   * Also clear mergedFrom on all tiles.
   */
  prepareTiles() {
    this.grid.eachCell(function (x, y, tile) {
      if (tile) {
        tile.mergedFrom = null;
        tile.savePosition();
      }
    });
  }

  /**
   * Rebuild the grid from a 2D value array (rows[y][x]),
   * preserving animation metadata (previousPosition, mergedFrom).
   */
  rebuildGrid(newRows) {
    var size = this.size;
    var oldGrid = this.grid;

    // Build a map of old tiles by position for animation tracking
    var oldTiles = {};
    oldGrid.eachCell(function (x, y, tile) {
      if (tile) {
        // Use the saved previousPosition (position before this move)
        var key = x + ',' + y;
        if (!oldTiles[key]) {
          oldTiles[key] = [];
        }
        oldTiles[key].push(tile);
      }
    });

    // Create a fresh grid
    this.grid = new Grid(size);

    for (var y = 0; y < size; y++) {
      for (var x = 0; x < size; x++) {
        var value = newRows[y][x];
        if (value !== 0) {
          var newTile = new Tile({ x: x, y: y }, value);

          // Find tiles that moved to this position
          var sourceTiles = this.findSourceTiles(oldGrid, x, y, value, newRows);

          if (sourceTiles.length === 2) {
            // This tile was produced by merging two tiles
            newTile.mergedFrom = sourceTiles;
            // Use one of the source tile's previous position
            newTile.previousPosition = sourceTiles[0].previousPosition || sourceTiles[0].position;
          } else if (sourceTiles.length === 1) {
            // This tile moved from another position
            newTile.previousPosition = sourceTiles[0].previousPosition || sourceTiles[0].position;
          }

          this.grid.insertTile(newTile);
        }
      }
    }
  }

  /**
   * Find source tiles from the old grid that contributed to the tile at (x, y)
   * in the new grid. For merged tiles, returns 2 source tiles.
   * For moved tiles, returns 1 source tile.
   */
  findSourceTiles(oldGrid, x, y, newValue, newRows) {
    var sources = [];
    var size = this.size;

    // Check if the old grid had a tile at the same position with the same value
    var oldTile = oldGrid.cellContent({ x: x, y: y });

    // Look for a merge: two tiles with half the new value
    var halfValue = newValue / 2;
    var potentialMergeSources = [];

    oldGrid.eachCell(function (ox, oy, tile) {
      if (tile && tile.value === halfValue) {
        potentialMergeSources.push(tile);
      }
    });

    // If old tile at same position had the same value, it just stayed or moved here
    if (oldTile && oldTile.value === newValue) {
      return [oldTile];
    }

    // If old tile at same position had half the value, this might be a merge
    if (oldTile && oldTile.value === halfValue && potentialMergeSources.length >= 2) {
      // Find another tile with the same half value
      for (var i = 0; i < potentialMergeSources.length; i++) {
        var src = potentialMergeSources[i];
        if (src !== oldTile) {
          return [oldTile, src];
        }
      }
    }

    // Tile moved from elsewhere
    oldGrid.eachCell(function (ox, oy, tile) {
      if (tile && tile.value === newValue && sources.length === 0) {
        sources.push(tile);
      }
    });

    return sources;
  }

  /**
   * Check if any tile on the grid has the given value.
   */
  hasTileValue(value) {
    var found = false;
    this.grid.eachCell(function (x, y, tile) {
      if (tile && tile.value === value) {
        found = true;
      }
    });
    return found;
  }

  /**
   * Check if the game is over: no empty cells AND no adjacent same-value tiles.
   */
  isGameOver() {
    // If there are empty cells, game is not over
    if (this.grid.emptyCells().length > 0) {
      return false;
    }

    var size = this.size;
    var grid = this.grid;

    // Check for any adjacent tiles with the same value
    for (var x = 0; x < size; x++) {
      for (var y = 0; y < size; y++) {
        var tile = grid.cellContent({ x: x, y: y });
        if (tile) {
          // Check right neighbor
          if (x + 1 < size) {
            var right = grid.cellContent({ x: x + 1, y: y });
            if (right && right.value === tile.value) {
              return false;
            }
          }
          // Check bottom neighbor
          if (y + 1 < size) {
            var below = grid.cellContent({ x: x, y: y + 1 });
            if (below && below.value === tile.value) {
              return false;
            }
          }
        }
      }
    }

    return true;
  }

  /**
   * Enable keep playing mode (continue after reaching 2048).
   */
  continueGame() {
    this.keepPlaying = true;
    this.actuate();
  }

  /**
   * Notify the renderer to update the display and update scores.
   */
  actuate() {
    if (this.renderer) {
      this.renderer.render(this.grid);
      this.renderer.updateScore(this.score);
      this.renderer.updateBestScore(this.bestScore);

      if (this.over) {
        this.renderer.showMessage(false); // game over, not won
      } else if (this.won && !this.keepPlaying) {
        this.renderer.showMessage(true); // won
      } else {
        this.renderer.clearMessage();
      }
    }
  }

  /**
   * Save the current game state via storageManager.
   */
  saveState() {
    if (this.storageManager) {
      this.storageManager.setGameState({
        grid: this.grid.serialize(),
        score: this.score,
        over: this.over,
        won: this.won,
        keepPlaying: this.keepPlaying
      });
    }
  }
}

// Conditional export for Node.js/test environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    moveLine,
    transposeGrid,
    reverseRows,
    gridToRows,
    applyMove,
    buildTraversals,
    addRandomTile,
    GameManager
  };
}
