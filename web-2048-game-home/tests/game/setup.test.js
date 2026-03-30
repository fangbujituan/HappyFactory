/**
 * Setup verification test — confirms the test environment works correctly.
 * Validates that:
 *   - vitest runs with jsdom environment
 *   - fast-check generators produce valid data
 *   - game modules can be imported via conditional exports
 */
const fc = require('fast-check');
const { tileValueArb, gridArb, directionArb, gameStateArb } = require('./generators');
const { Tile } = require('../../js/tile');
const { Grid } = require('../../js/grid');
const { moveLine, GameManager } = require('../../js/game-manager');
const { StorageManager } = require('../../js/storage-manager');

describe('Test environment setup', () => {
  test('fast-check is available and generators work', () => {
    // Verify tileValueArb produces valid tile values
    fc.assert(
      fc.property(tileValueArb, (value) => {
        return [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048].includes(value);
      }),
      { numRuns: 50 }
    );
  });

  test('gridArb generates 4x4 grids', () => {
    fc.assert(
      fc.property(gridArb, (grid) => {
        return grid.length === 4 && grid.every(col => col.length === 4);
      }),
      { numRuns: 50 }
    );
  });

  test('directionArb generates valid directions', () => {
    fc.assert(
      fc.property(directionArb, (dir) => {
        return [0, 1, 2, 3].includes(dir);
      }),
      { numRuns: 20 }
    );
  });

  test('gameStateArb generates valid game states', () => {
    fc.assert(
      fc.property(gameStateArb, (state) => {
        return (
          state.grid.length === 4 &&
          typeof state.score === 'number' &&
          typeof state.over === 'boolean' &&
          typeof state.won === 'boolean' &&
          typeof state.keepPlaying === 'boolean'
        );
      }),
      { numRuns: 50 }
    );
  });

  test('Tile class is importable and functional', () => {
    const tile = new Tile({ x: 1, y: 2 }, 4);
    expect(tile.position).toEqual({ x: 1, y: 2 });
    expect(tile.value).toBe(4);
  });

  test('Grid class is importable and functional', () => {
    const grid = new Grid(4);
    expect(grid.size).toBe(4);
    expect(grid.emptyCells().length).toBe(16);
  });

  test('moveLine function is importable and functional', () => {
    const result = moveLine([2, 2, 4, 4]);
    expect(result.line).toEqual([4, 8, 0, 0]);
    expect(result.score).toBe(12);
  });

  test('StorageManager is importable', () => {
    expect(typeof StorageManager).toBe('function');
  });
});
