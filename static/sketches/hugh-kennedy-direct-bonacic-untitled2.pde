int columns = 32;
int rows = 32;
int margin = 32;
int padding = 8;
int squareWidth = 8;
int squareHeight = 8;

int[][] tValues = {
  { 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 26, 9000 },
  { 0, 31, 94, 93, 91, 90, 89, 9000, 8, 9, 10, 11, 28, 33, 34, 35, 36, 37, 38, 39 },
  { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 900, 12010, 12011 },
  { 5, 6, 19, 18 }
};

void drawGrid(int gridX, int gridY, int[] squares) {
  stroke(0);
  fill(0);

  rect(
    gridX - padding,
    gridY - padding,
    squareWidth * columns + padding * 2,
    squareHeight * rows + padding * 2
  );

  fill(255);

  int t, y;

  for (int i = 0, l = squares.length; i < l; i += 1) {
    t = squares[i];

    for (int x = 0; x < columns; x += 1) {
      y = (x ^ t) % rows;

      rect(
        gridX + x * squareWidth,
        gridY + y * squareHeight,
        squareWidth,
        squareHeight
      );
    }
  }
}

void setup() {
  size(
    2 * columns * squareWidth + 3 * margin,
    2 * rows * squareHeight + 3 * margin
  );
  noLoop();
}

void draw() {
  background(255);
  for (int i = 0; i < tValues.length; i += 1) {
    drawGrid(
      (i % 2) * (columns * squareWidth + margin) + margin,
      floor(i / 2) * (rows * squareHeight + margin) + margin,
      tValues[i]
    );
  }
}
