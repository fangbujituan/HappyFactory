/**
 * Shared fast-check generators for 2048 game property tests.
 *
 * These generators produce random valid game data for use across
 * all property-based test files.
 */
const fc = require('fast-check');

// Valid tile values (powers of 2 from 2 to 2048)
const tileValueArb = fc.constantFrom(2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048);

// A single cell: either null (empty) or a tile value
const cellArb = fc.oneof(fc.constant(null), tileValueArb);

// A 4x4 grid of cells (columns × rows, matching cells[x][y] convention)
const gridArb = fc.array(fc.array(cellArb, { minLength: 4, maxLength: 4 }), { minLength: 4, maxLength: 4 });

// Movement direction: 0=up, 1=right, 2=down, 3=left
const directionArb = fc.constantFrom(0, 1, 2, 3);

// Complete game state
const gameStateArb = fc.record({
  grid: gridArb,
  score: fc.nat(),
  over: fc.boolean(),
  won: fc.boolean(),
  keepPlaying: fc.boolean()
});

// A single row/line of 4 values (0 = empty, otherwise tile value)
const lineArb = fc.array(
  fc.oneof(fc.constant(0), tileValueArb),
  { minLength: 4, maxLength: 4 }
);

// A non-empty grid (at least one tile present)
const nonEmptyGridArb = gridArb.filter(grid => {
  for (let x = 0; x < 4; x++) {
    for (let y = 0; y < 4; y++) {
      if (grid[x][y] !== null) return true;
    }
  }
  return false;
});

module.exports = {
  tileValueArb,
  cellArb,
  gridArb,
  directionArb,
  gameStateArb,
  lineArb,
  nonEmptyGridArb
};
